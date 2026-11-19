import sqlite3
import urllib.request
import urllib.parse
import json
import time
import re

API_KEY = "47861caa-b7aa-4d20-9ee3-9a2f1179eea3"
HEADERS = {
    "X-API-Key": API_KEY,
    "User-Agent": "Mozilla/5.0"
}

def clean_query(prod_name: str, mp_name: str) -> str:
    # Clean product names for optimal search in QuickCommerceAPI
    name = prod_name
    name = re.sub(r'\(.*?\)', '', name) # remove parentheses e.g. (GPS, 46mm)
    name = re.sub(r'Founders Edition', '', name)
    name = re.sub(r'Full-Frame Mirrorless Camera', 'Camera', name)
    name = re.sub(r'Smart TV', 'TV', name)
    name = name.strip()
    return name

def find_best_match(products, target_name: str):
    if not products:
        return None
    
    target_words = set(re.findall(r'\w+', target_name.lower()))
    
    # Negative keywords if target is not an accessory
    is_accessory = any(x in target_name.lower() for x in ["case", "cover", "glass", "strap"])
    negatives = ["case", "cover", "tempered", "glass", "skin", "adapter", "cable", "strap", "guard", "pouch"]
    
    candidates = []
    for p in products:
        p_name = p.get("name", "").lower()
        deeplink = p.get("deeplink", "")
        if not deeplink or "search" in deeplink:
            continue
            
        # If target is not an accessory, penalize accessories
        if not is_accessory and any(neg in p_name for neg in negatives):
            continue
            
        # Count word matches
        p_words = set(re.findall(r'\w+', p_name))
        overlap = len(target_words.intersection(p_words))
        
        # Exact number checks (e.g. 9 in Pixel 9 vs Pixel 11, or 16 in iPhone 16)
        numbers_in_target = set(re.findall(r'\b\d+\b', target_name))
        numbers_in_p = set(re.findall(r'\b\d+\b', p.get("name", "")))
        if numbers_in_target and not numbers_in_target.issubset(numbers_in_p):
            overlap -= 2
            
        candidates.append((overlap, p))
        
    if not candidates:
        # Fallback to the first non-accessory result or first result
        for p in products:
            p_name = p.get("name", "").lower()
            if not is_accessory and any(neg in p_name for neg in negatives):
                continue
            return p
        return products[0]
        
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]

def query_qc_api(query_str: str, platform: str):
    q = urllib.parse.quote(query_str)
    url = f"https://api.quickcommerceapi.com/v1/search?q={q}&platform={platform}&lat=28.6139&lon=77.2090"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return data
    except Exception as e:
        print(f"Error querying {query_str} on {platform}: {e}")
        return None

def main():
    conn = sqlite3.connect("backend/pricewise.db")
    cur = conn.cursor()
    
    cur.execute("""
        SELECT l.id, p.name, m.slug, l.product_url, p.slug
        FROM marketplace_listings l
        JOIN product_variants v ON v.id = l.variant_id
        JOIN products p ON p.id = v.product_id
        JOIN marketplaces m ON m.id = l.marketplace_id
        ORDER BY p.name, m.slug
    """)
    rows = cur.fetchall()
    
    print(f"Found {len(rows)} listings in database.")
    
    exact_links_map = {}
    updated_count = 0
    skipped_count = 0
    
    for listing_id, prod_name, mp_slug, current_url, p_slug in rows:
        platform = "Amazon" if "amazon" in mp_slug.lower() else "Flipkart"
        
        # Check if already an exact direct link (not a search link)
        if current_url and "/s?k=" not in current_url and "/search?q=" not in current_url and ("/dp/" in current_url or "/p/" in current_url or "pid=" in current_url):
            print(f"[KEEP EXISTING EXACT] {prod_name} on {platform} -> {current_url}")
            exact_links_map.setdefault(p_slug, {})[platform.lower()] = current_url
            skipped_count += 1
            continue
            
        search_q = clean_query(prod_name, platform)
        print(f"\n[QUERYING QC API] '{search_q}' for {platform}...")
        
        data = query_qc_api(search_q, platform)
        if not data:
            continue
            
        rem = data.get("credits_remaining")
        print(f"  Credits remaining: {rem}")
        products = data.get("data", {}).get("products", [])
        
        best = find_best_match(products, prod_name)
        if best and best.get("deeplink"):
            exact_url = best.get("deeplink")
            price = best.get("offer_price")
            mrp = best.get("mrp")
            matched_name = best.get("name")
            print(f"  Matched: '{matched_name}'")
            print(f"  EXACT URL: {exact_url}")
            print(f"  Price: {price} (MRP: {mrp})")
            
            # Update database listing with exact URL
            cur.execute("""
                UPDATE marketplace_listings 
                SET product_url = ?, current_price = COALESCE(?, current_price), original_mrp = COALESCE(?, original_mrp)
                WHERE id = ?
            """, (exact_url, price, mrp, listing_id))
            
            exact_links_map.setdefault(p_slug, {})[platform.lower()] = exact_url
            updated_count += 1
        else:
            print(f"  No suitable direct match found for {prod_name}")
            
        time.sleep(0.5)  # slight pause between calls
        
    conn.commit()
    conn.close()
    
    print("\n==========================================")
    print(f"Processing Complete!")
    print(f"Updated listings with exact links: {updated_count}")
    print(f"Preserved existing verified links: {skipped_count}")
    print("==========================================")
    
    # Save exact map to a JSON file for inspection & permanent reference
    with open("scripts/exact_catalog_links.json", "w") as f:
        json.dump(exact_links_map, f, indent=2)
    print("Saved exact catalog links to scripts/exact_catalog_links.json")

if __name__ == "__main__":
    main()
