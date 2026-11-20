import sqlite3
import json
import os

BAD_PRODUCT_NAMES = [
    "Cotton Earbuds",
    "Cotton Buds (Paper Stick)",
    "Ear Cleaner Tool Kit",
    "Simply Disposable Women's Razor",
    "Presto 2-Blade Smoother Shaving Men's Razor",
    "Sensi Smart 3 Men's Razor",
    "Guard Manual Shaving Men's Razor - with Blades"
]

def clean_database(db_path):
    if not os.path.exists(db_path):
        print(f"Skipping {db_path} (does not exist)")
        return

    print(f"\nCleaning database: {db_path}")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # 1. Fix ASUS TUF Flipkart listing
    c.execute("""
        UPDATE marketplace_listings
        SET current_price = 49990.0,
            original_mrp = 78990.0
        WHERE current_price <= 0
    """)
    updated_listings = c.rowcount
    print(f"Updated {updated_listings} zero-price listings to ₹49,990 (ASUS TUF).")

    # Update price_history for ASUS TUF if any has price <= 0
    c.execute("UPDATE price_history SET price = 49990.0 WHERE price <= 0")
    print(f"Updated {c.rowcount} zero-price price_history records.")

    # 2. Find and delete bad non-electronics products
    deleted_count = 0
    for name in BAD_PRODUCT_NAMES:
        c.execute("SELECT id FROM products WHERE name = ?", (name,))
        p_rows = c.fetchall()
        for (pid,) in p_rows:
            # find variants
            c.execute("SELECT id FROM product_variants WHERE product_id = ?", (pid,))
            v_rows = c.fetchall()
            for (vid,) in v_rows:
                # find listings
                c.execute("SELECT id FROM marketplace_listings WHERE variant_id = ?", (vid,))
                l_rows = c.fetchall()
                for (lid,) in l_rows:
                    c.execute("DELETE FROM price_history WHERE listing_id = ?", (lid,))
                    c.execute("DELETE FROM reviews WHERE listing_id = ?", (lid,))
                c.execute("DELETE FROM marketplace_listings WHERE variant_id = ?", (vid,))
                c.execute("DELETE FROM specifications WHERE variant_id = ?", (vid,))
            c.execute("DELETE FROM product_variants WHERE product_id = ?", (pid,))
            c.execute("DELETE FROM products WHERE id = ?", (pid,))
            deleted_count += 1
            print(f"Deleted non-electronic product: {name} (ID: {pid})")

    conn.commit()

    # Check remaining count
    c.execute("SELECT count(*) FROM products")
    total_products = c.fetchone()[0]
    print(f"Remaining products in {db_path}: {total_products}")

    # Check for any remaining price <= 0
    c.execute("SELECT count(*) FROM marketplace_listings WHERE current_price <= 0")
    bad_prices = c.fetchone()[0]
    print(f"Remaining listings with price <= 0: {bad_prices}")

    conn.close()


def clean_seed_catalog(json_path):
    if not os.path.exists(json_path):
        print(f"Skipping {json_path}")
        return

    print(f"\nCleaning seed catalog: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned = []
    for item in data:
        name = item.get("name", "")
        if name in BAD_PRODUCT_NAMES:
            print(f"Filtered out seed item: {name}")
            continue

        # Fix ASUS TUF 0 price
        if name == "ASUS TUF Gaming F15" and item.get("price", 0) <= 0:
            item["price"] = 49990.0
            item["mrp"] = 78990.0
            print("Fixed ASUS TUF Flipkart seed entry to ₹49,990")

        cleaned.append(item)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

    print(f"Updated {json_path}: previous {len(data)} items -> now {len(cleaned)} items.")


if __name__ == "__main__":
    clean_database("pricewise.db")
    clean_database("backend/pricewise.db")
    clean_seed_catalog("backend/data/seed_catalog.json")
    print("\nAll database cleanups and fixes completed successfully.")
