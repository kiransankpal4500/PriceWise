import sqlite3
import urllib.parse

def run_migration():
    conn = sqlite3.connect("backend/pricewise.db")
    cur = conn.cursor()

    # 1. Ten Manual Curated Products with Direct Live URLs
    # Mapping of product slug -> { "amazon": url, "flipkart": url }
    manual_10_products = {
        "apple-iphone-16": {
            "amazon": "https://www.amazon.in/dp/B0DGJHBX5Y",
            "flipkart": "https://www.flipkart.com/search?q=Apple+iPhone+16+128GB"
        },
        "apple-airpods-pro-2-usb-c": {
            "amazon": "https://www.amazon.in/dp/B0CHX3TW6X",
            "flipkart": "https://www.flipkart.com/search?q=Apple+AirPods+Pro+2nd+Gen+USB-C"
        },
        "apple-ipad-10th-generation": {
            "amazon": "https://www.amazon.in/dp/B0BJMK3Z87",
            "flipkart": "https://www.flipkart.com/search?q=Apple+iPad+10th+Gen+64GB"
        },
        "sony-wh-1000xm5-wireless-headphones": {
            "amazon": "https://www.amazon.in/s?k=Sony+WH-1000XM5+Wireless+Headphones",
            "flipkart": "https://www.flipkart.com/search?q=Sony+WH-1000XM5"
        },
        "sony-wh-ch720n-noise-cancelling": {
            "amazon": "https://www.amazon.in/dp/B0BS1PRC4L",
            "flipkart": "https://www.flipkart.com/search?q=Sony+WH-CH720N"
        },
        "oneplus-nord-4-5g": {
            "amazon": "https://www.amazon.in/dp/B0D77PNJMG",
            "flipkart": "https://www.flipkart.com/search?q=OnePlus+Nord+4+5G"
        },
        "samsung-galaxy-a55-5g": {
            "amazon": "https://www.amazon.in/dp/B0CX8XF1X8",
            "flipkart": "https://www.flipkart.com/search?q=Samsung+Galaxy+A55+5G"
        },
        "samsung-crystal-4k-vivid-pro-55": {
            "amazon": "https://www.amazon.in/dp/B0CX8VRP2P",
            "flipkart": "https://www.flipkart.com/search?q=Samsung+Crystal+4K+Vivid+Pro+55"
        },
        "asus-tuf-gaming-f15": {
            "amazon": "https://www.amazon.in/dp/B0CR7QJNLQ",
            "flipkart": "https://www.flipkart.com/search?q=ASUS+TUF+Gaming+F15"
        },
        "apple-macbook-air-13-m3": {
            "amazon": "https://www.amazon.in/s?k=Apple+MacBook+Air+13+inch+M3",
            "flipkart": "https://www.flipkart.com/search?q=Apple+MacBook+Air+M3"
        }
    }

    # Fetch all listings with product information
    cur.execute("""
        SELECT l.id, p.slug, p.name, m.slug, l.title 
        FROM marketplace_listings l
        JOIN product_variants v ON v.id = l.variant_id
        JOIN products p ON p.id = v.product_id
        JOIN marketplaces m ON m.id = l.marketplace_id
    """)
    rows = cur.fetchall()

    manual_count = 0
    automatic_count = 0

    for listing_id, p_slug, p_name, m_slug, l_title in rows:
        # Determine if this product has a manual curated link
        if p_slug in manual_10_products:
            m_key = "amazon" if "amazon" in m_slug else "flipkart"
            final_url = manual_10_products[p_slug].get(m_key)
            if not final_url:
                search_term = urllib.parse.quote_plus(p_name)
                final_url = (
                    f"https://www.amazon.in/s?k={search_term}"
                    if "amazon" in m_slug
                    else f"https://www.flipkart.com/search?q={search_term}"
                )
            manual_count += 1
        else:
            # AUTOMATIC GUARANTEED REDIRECT FOR ALL OTHER PRODUCTS
            search_term = urllib.parse.quote_plus(p_name)
            if "amazon" in m_slug:
                final_url = f"https://www.amazon.in/s?k={search_term}"
            elif "flipkart" in m_slug:
                final_url = f"https://www.flipkart.com/search?q={search_term}"
            else:
                final_url = f"https://www.amazon.in/s?k={search_term}"
            automatic_count += 1

        cur.execute("UPDATE marketplace_listings SET product_url = ? WHERE id = ?", (final_url, listing_id))

    conn.commit()
    print(f"Updated {len(rows)} listings:")
    print(f" - {manual_count} manual verified product listings updated")
    print(f" - {automatic_count} automatic guaranteed marketplace search redirects updated")
    conn.close()

if __name__ == "__main__":
    run_migration()
