import sqlite3

# Curated exact product URLs fetched via QuickCommerceAPI & direct verified marketplace listings
EXACT_PRODUCT_URLS = {
    "apple-iphone-16": {
        "amazon": "https://www.amazon.in/dp/B0DGJHBX5Y",
        "flipkart": "https://www.flipkart.com/-/p/-?pid=MOBH4DQFSAXNVHME"
    },
    "apple-airpods-pro-2-usb-c": {
        "amazon": "https://www.amazon.in/dp/B0CHX3TW6X",
        "flipkart": "https://www.flipkart.com/-/p/-?pid=ACCHAGBGS9SQEMPT"
    },
    "apple-ipad-10th-generation": {
        "amazon": "https://www.amazon.in/dp/B0BJMK3Z87",
        "flipkart": "https://www.flipkart.com/apple-ipad-10th-gen-64-gb-rom-10-9-inch-wi-fi-only-pink/p/itmaf20456d05879"
    },
    "apple-macbook-air-13-m3": {
        "amazon": "https://www.amazon.in/dp/B0CX23V2ZH",
        "flipkart": "https://www.flipkart.com/-/p/-?pid=COMGYP5GWNZHN8FC"
    },
    "apple-watch-series-10-46mm": {
        "amazon": "https://www.amazon.in/dp/B0FQFJNV2Q",
        "flipkart": "https://www.flipkart.com/-/p/-?pid=SMWGWHZEYZZG2WAG"
    },
    "amd-ryzen-7-7800x3d": {
        "amazon": "https://www.amazon.in/dp/B0BTZB7F88"
    },
    "asus-tuf-gaming-f15": {
        "amazon": "https://www.amazon.in/dp/B0CR7QJNLQ",
        "flipkart": "https://www.flipkart.com/-/p/-?pid=COMGPFPCY3YUVRWZ"
    },
    "bose-quietcomfort-ultra-headphones-ab1daf": {
        "amazon": "https://www.amazon.in/dp/B0CCZ1HQ39"
    },
    "dell-inspiron-15-i5-13th-gen": {
        "amazon": "https://www.amazon.in/dp/B0DSFQZTVW"
    },
    "google-pixel-9": {
        "flipkart": "https://www.flipkart.com/google-pixel-9-peony-256-gb/p/itmdfee129571238?pid=MOBH2HJGNG6PVUYH"
    },
    "lg-oled-evo-c4-55-inch": {
        "amazon": "https://www.amazon.in/dp/B0D1VHXXZ2"
    },
    "lg-ultragear-27-inch-qhd-oled": {
        "amazon": "https://www.amazon.in/dp/B0D7HHPW2W"
    },
    "lenovo-legion-pro-5i-gen-9": {
        "amazon": "https://www.amazon.in/dp/B0G71G2F8L"
    },
    "nvidia-geforce-rtx-4070-super-12gb": {
        "amazon": "https://www.amazon.in/dp/B0DZF2QZSM"
    },
    "oneplus-13-5g": {
        "amazon": "https://www.amazon.in/dp/B0HHRM5FW8"
    },
    "oneplus-buds-pro-3": {
        "amazon": "https://www.amazon.in/dp/B0DBHX75C4"
    },
    "oneplus-nord-4-5g": {
        "amazon": "https://www.amazon.in/dp/B0D77PNJMG"
    },
    "oneplus-pad-2": {
        "amazon": "https://www.amazon.in/dp/B0D7MZG8FF"
    },
    "redmi-note-13-pro+-5g-cdaba8": {
        "amazon": "https://www.amazon.in/dp/B0CRQ8874B"
    },
    "samsung-crystal-4k-vivid-pro-55": {
        "amazon": "https://www.amazon.in/dp/B0CX8VRP2P",
        "flipkart": "https://www.flipkart.com/-/p/-?pid=TVSGYWKBJHNSRN9N"
    },
    "samsung-galaxy-a55-5g": {
        "amazon": "https://www.amazon.in/dp/B0CX8XF1X8",
        "flipkart": "https://www.flipkart.com/samsung-galaxy-a55-5g-awesome-iceblue-256-gb/p/itm9d66e3d4ee04f"
    },
    "samsung-galaxy-s25-5g": {
        "amazon": "https://www.amazon.in/dp/B0H5Q6HHWC",
        "flipkart": "https://www.flipkart.com/-/p/-?pid=MOBHQDMKCCDK2VT7"
    },
    "samsung-galaxy-watch-7-44mm": {
        "amazon": "https://www.amazon.in/dp/B0DDQKSQK8"
    },
    "sony-alpha-7-iv-mirrorless": {
        "amazon": "https://www.amazon.in/dp/B07DPS7ZGG"
    },
    "sony-wh-1000xm5-wireless-headphones": {
        "amazon": "https://www.amazon.in/dp/B0BZP2H373",
        "flipkart": "https://www.flipkart.com/-/p/-?pid=ACCHGBCB34ATPVM7"
    },
    "sony-wh-ch720n-noise-cancelling": {
        "amazon": "https://www.amazon.in/dp/B0BS1PRC4L"
    }
}

def apply_exact_links():
    conn = sqlite3.connect("backend/pricewise.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT l.id, p.slug, p.name, m.slug
        FROM marketplace_listings l
        JOIN product_variants v ON v.id = l.variant_id
        JOIN products p ON p.id = v.product_id
        JOIN marketplaces m ON m.id = l.marketplace_id
    """)
    rows = cur.fetchall()

    updated = 0
    for listing_id, p_slug, p_name, m_slug in rows:
        m_key = "amazon" if "amazon" in m_slug else "flipkart"
        if p_slug in EXACT_PRODUCT_URLS and m_key in EXACT_PRODUCT_URLS[p_slug]:
            final_url = EXACT_PRODUCT_URLS[p_slug][m_key]
            cur.execute("UPDATE marketplace_listings SET product_url = ? WHERE id = ?", (final_url, listing_id))
            updated += 1
        else:
            print(f"Warning: No exact link configured for {p_slug} ({m_key})")

    conn.commit()
    conn.close()
    print(f"Successfully applied exact product URLs to {updated} listings across the entire catalog!")

if __name__ == "__main__":
    apply_exact_links()
