import sqlite3

conn = sqlite3.connect("pricewise.db")
c = conn.cursor()

# 1. Check for 0 or negative prices
c.execute("""
    SELECT p.name, p.slug, ml.current_price, ml.original_mrp, ml.product_url, m.name
    FROM products p
    JOIN product_variants pv ON pv.product_id = p.id
    JOIN marketplace_listings ml ON ml.variant_id = pv.id
    JOIN marketplaces m ON m.id = ml.marketplace_id
    WHERE ml.current_price <= 0 OR ml.current_price IS NULL
""")
zero_prices = c.fetchall()
print(f"\n--- Found {len(zero_prices)} listings with price <= 0: ---")
for r in zero_prices[:10]:
    print(r)

# 2. Check ASUS TUF specifically
c.execute("""
    SELECT p.name, p.slug, ml.current_price, ml.original_mrp, ml.product_url, m.name
    FROM products p
    JOIN product_variants pv ON pv.product_id = p.id
    JOIN marketplace_listings ml ON ml.variant_id = pv.id
    JOIN marketplaces m ON m.id = ml.marketplace_id
    WHERE p.name LIKE '%ASUS TUF%'
""")
tuf = c.fetchall()
print(f"\n--- ASUS TUF Gaming listings ({len(tuf)}): ---")
for r in tuf:
    print(r)

# 3. Check for non-electronics (razors, cotton buds, etc.)
c.execute("""
    SELECT p.id, p.name, c.name, m.name, ml.product_url
    FROM products p
    JOIN categories c ON c.id = p.category_id
    JOIN product_variants pv ON pv.product_id = p.id
    JOIN marketplace_listings ml ON ml.variant_id = pv.id
    JOIN marketplaces m ON m.id = ml.marketplace_id
    WHERE p.name LIKE '%razor%'
       OR p.name LIKE '%cotton bud%'
       OR p.name LIKE '%shaving%'
       OR p.name LIKE '%gillette%'
""")
non_elec = c.fetchall()
print(f"\n--- Non-electronics found ({len(non_elec)}): ---")
for r in non_elec:
    print(r)

# 4. Check for search links vs direct links
c.execute("""
    SELECT COUNT(*) FROM marketplace_listings WHERE product_url LIKE '%/s?k=%' OR product_url LIKE '%search%'
""")
search_links_count = c.fetchone()[0]
print(f"\n--- Listings with search query links: {search_links_count} ---")

c.execute("""
    SELECT p.name, ml.product_url, m.name
    FROM products p
    JOIN product_variants pv ON pv.product_id = p.id
    JOIN marketplace_listings ml ON ml.variant_id = pv.id
    JOIN marketplaces m ON m.id = ml.marketplace_id
    WHERE ml.product_url LIKE '%/s?k=%' OR ml.product_url LIKE '%search%'
    LIMIT 10
""")
sample_search_links = c.fetchall()
for r in sample_search_links:
    print(r)
