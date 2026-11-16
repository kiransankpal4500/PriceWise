"""
High-fidelity commercial-grade seed catalog for PriceWise covering 10 electronics categories in India
with authentic INR pricing, detailed technical specifications, multiple hardware variants, and listings for Amazon India and Flipkart.
"""

SEED_CATEGORIES = [
    {"name": "Smartphones", "slug": "smartphones", "description": "Flagship, upper-midrange, and budget smartphones", "icon_name": "Smartphone"},
    {"name": "Laptops", "slug": "laptops", "description": "Ultrabooks, creator workstations, and gaming laptops", "icon_name": "Laptop"},
    {"name": "Tablets", "slug": "tablets", "description": "Productivity, media, and digital art tablets", "icon_name": "Tablet"},
    {"name": "Smartwatches", "slug": "smartwatches", "description": "Fitness trackers and flagship wearables", "icon_name": "Watch"},
    {"name": "Earbuds", "slug": "earbuds", "description": "True wireless stereo (TWS) noise cancelling earbuds", "icon_name": "Headphones"},
    {"name": "Headphones", "slug": "headphones", "description": "Over-ear audiophile and noise-cancelling headphones", "icon_name": "Headphones"},
    {"name": "Monitors", "slug": "monitors", "description": "High-refresh gaming and color-accurate professional monitors", "icon_name": "Monitor"},
    {"name": "Televisions", "slug": "televisions", "description": "4K OLED, QLED, and Mini-LED smart displays", "icon_name": "Tv"},
    {"name": "Cameras", "slug": "cameras", "description": "Mirrorless and cinema professional cameras", "icon_name": "Camera"},
    {"name": "Computer Components", "slug": "computer-components", "description": "Processors, graphics cards, RAM, and PCIe SSDs", "icon_name": "Cpu"},
]

SEED_BRANDS = [
    {"name": "Apple", "slug": "apple", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg"},
    {"name": "Samsung", "slug": "samsung", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/2/24/Samsung_Logo.svg"},
    {"name": "OnePlus", "slug": "oneplus", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/8/82/OnePlus_Logo.svg"},
    {"name": "Google", "slug": "google", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg"},
    {"name": "Sony", "slug": "sony", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/c/ca/Sony_logo.svg"},
    {"name": "Dell", "slug": "dell", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/1/18/Dell_logo_2016.svg"},
    {"name": "Lenovo", "slug": "lenovo", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/b/b8/Lenovo_logo_2015.svg"},
    {"name": "ASUS", "slug": "asus", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/2/2e/ASUS_Logo.svg"},
    {"name": "LG", "slug": "lg", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/b/bf/LG_logo_%282015%29.svg"},
    {"name": "NVIDIA", "slug": "nvidia", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/2/21/Nvidia_logo.svg"},
    {"name": "Xiaomi", "slug": "xiaomi", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/a/ae/Xiaomi_logo_%282021-%29.svg"},
    {"name": "Bose", "slug": "bose", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/0/02/Bose_logo.svg"},
    {"name": "Canon", "slug": "canon", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/7/75/Canon_wordmark.svg"},
    {"name": "AMD", "slug": "amd", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/7/7c/AMD_Logo.svg"},
]

SEED_MARKETPLACES = [
    {"name": "Amazon India", "slug": "amazon", "base_url": "https://www.amazon.in", "logo_url": "/marketplaces/amazon.png"},
    {"name": "Flipkart", "slug": "flipkart", "base_url": "https://www.flipkart.com", "logo_url": "/marketplaces/flipkart.png"},
]

SEED_PRODUCTS = [
    # ==========================================
    # 1. SMARTPHONES
    # ==========================================
    {
        "category_slug": "smartphones",
        "brand_slug": "samsung",
        "name": "Samsung Galaxy S25 5G",
        "slug": "samsung-galaxy-s25-5g",
        "model_number": "SM-S931B",
        "description": "Next-gen compact flagship with Snapdragon 8 Elite, Galaxy AI, and 50MP triple camera system.",
        "default_image_url": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?auto=format&fit=crop&w=800&q=80",
        "variants": [
            {
                "name": "128GB Storage, 12GB RAM, Onyx Black",
                "sku": "S25-128-BLK",
                "ram": "12GB",
                "storage": "128GB",
                "color": "Onyx Black",
                "mrp": 79999.00,
                "specs": [
                    {"group": "Performance", "name": "Processor", "value": "Qualcomm Snapdragon 8 Elite (3nm)"},
                    {"group": "Display", "name": "Screen Size", "value": "6.2 inches Dynamic AMOLED 2X, 120Hz LTPO"},
                    {"group": "Camera", "name": "Rear Camera", "value": "50MP (Wide, OIS) + 10MP (Telephoto 3x) + 12MP (Ultrawide)"},
                    {"group": "Battery", "name": "Battery Capacity", "value": "4000 mAh with 25W Fast Charging"},
                ],
                "listings": [
                    {"marketplace_slug": "amazon", "external_id": "B0DXS25AMZ1", "title": "Samsung Galaxy S25 5G (Onyx Black, 12GB RAM, 128GB Storage)", "product_url": "https://www.amazon.in/dp/B0DXS25AMZ1", "current_price": 74999.00, "original_mrp": 79999.00, "availability": "IN_STOCK", "seller_name": "Appario Retail India", "rating": 4.6, "review_count": 1420},
                    {"marketplace_slug": "flipkart", "external_id": "MOBHX928S25FK1", "title": "SAMSUNG Galaxy S25 5G (Onyx Black, 128 GB) (12 GB RAM)", "product_url": "https://www.flipkart.com/samsung-galaxy-s25-5g-onyx-black-128-gb/p/itmdxs25", "current_price": 73999.00, "original_mrp": 79999.00, "availability": "IN_STOCK", "seller_name": "TrueCom Retail", "rating": 4.5, "review_count": 980}
                ]
            },
            {
                "name": "256GB Storage, 12GB RAM, Marble Gray",
                "sku": "S25-256-GRY",
                "ram": "12GB",
                "storage": "256GB",
                "color": "Marble Gray",
                "mrp": 84999.00,
                "specs": [
                    {"group": "Performance", "name": "Processor", "value": "Qualcomm Snapdragon 8 Elite (3nm)"},
                    {"group": "Display", "name": "Screen Size", "value": "6.2 inches Dynamic AMOLED 2X, 120Hz LTPO"},
                ],
                "listings": [
                    {"marketplace_slug": "amazon", "external_id": "B0DXS25AMZ2", "title": "Samsung Galaxy S25 5G (Marble Gray, 12GB RAM, 256GB Storage)", "product_url": "https://www.amazon.in/dp/B0DXS25AMZ2", "current_price": 79999.00, "original_mrp": 84999.00, "availability": "IN_STOCK", "seller_name": "Appario Retail India", "rating": 4.7, "review_count": 840}
                ]
            }
        ]
    },
    {
        "category_slug": "smartphones",
        "brand_slug": "apple",
        "name": "Apple iPhone 16",
        "slug": "apple-iphone-16",
        "model_number": "A3287",
        "description": "Apple Intelligence enabled iPhone with A18 chip, Camera Control button, and 48MP Fusion camera.",
        "default_image_url": "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?auto=format&fit=crop&w=800&q=80",
        "variants": [
            {
                "name": "128GB Storage, Ultramarine",
                "sku": "IPHONE16-128-BLU",
                "ram": "8GB",
                "storage": "128GB",
                "color": "Ultramarine",
                "mrp": 79900.00,
                "specs": [
                    {"group": "Performance", "name": "Processor", "value": "Apple A18 Bionic (3nm)"},
                    {"group": "Display", "name": "Screen Size", "value": "6.1 inches Super Retina XDR OLED"},
                    {"group": "Camera", "name": "Rear Camera", "value": "48MP Fusion + 12MP Ultra Wide with Macro"},
                    {"group": "Special Features", "name": "AI", "value": "Apple Intelligence built-in"},
                ],
                "listings": [
                    {"marketplace_slug": "amazon", "external_id": "B0DGJ68G9H", "title": "Apple iPhone 16 (128 GB) - Ultramarine", "product_url": "https://www.amazon.in/dp/B0DGJ68G9H", "current_price": 76999.00, "original_mrp": 79900.00, "availability": "IN_STOCK", "seller_name": "Amazon Authorized Reseller", "rating": 4.7, "review_count": 3150},
                    {"marketplace_slug": "flipkart", "external_id": "MOBH8483IPH16", "title": "Apple iPhone 16 (Ultramarine, 128 GB)", "product_url": "https://www.flipkart.com/apple-iphone-16-ultramarine-128-gb/p/itmd83", "current_price": 76499.00, "original_mrp": 79900.00, "availability": "IN_STOCK", "seller_name": "SuperComNet", "rating": 4.7, "review_count": 2890}
                ]
            }
        ]
    },
    {
        "category_slug": "smartphones",
        "brand_slug": "oneplus",
        "name": "OnePlus 13 5G",
        "slug": "oneplus-13-5g",
        "model_number": "CPH2653",
        "description": "All-round flagship with Snapdragon 8 Elite, 6000mAh battery, and Hasselblad camera system.",
        "default_image_url": "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?auto=format&fit=crop&w=800&q=80",
        "variants": [
            {
                "name": "256GB Storage, 12GB RAM, Midnight Ocean",
                "sku": "OP13-256-BLU",
                "ram": "12GB",
                "storage": "256GB",
                "color": "Midnight Ocean",
                "mrp": 69999.00,
                "specs": [
                    {"group": "Performance", "name": "Processor", "value": "Qualcomm Snapdragon 8 Elite (3nm)"},
                    {"group": "Display", "name": "Screen Size", "value": "6.82 inches 2K ProXDR Display, 120Hz LTPO"},
                    {"group": "Camera", "name": "Rear Camera", "value": "50MP Sony LYT-808 + 50MP Periscope + 50MP Ultrawide"},
                    {"group": "Battery", "name": "Battery Capacity", "value": "6000 mAh with 100W SuperVOOC"},
                ],
                "listings": [
                    {"marketplace_slug": "amazon", "external_id": "B0DN83KOP13", "title": "OnePlus 13 5G (Midnight Ocean, 12GB RAM, 256GB Storage)", "product_url": "https://www.amazon.in/dp/B0DN83KOP13", "current_price": 64999.00, "original_mrp": 69999.00, "availability": "IN_STOCK", "seller_name": "OnePlus Official Store", "rating": 4.6, "review_count": 890}
                ]
            }
        ]
    },
    {
        "category_slug": "smartphones",
        "brand_slug": "google",
        "name": "Google Pixel 9",
        "slug": "google-pixel-9",
        "model_number": "G1D42",
        "description": "Engineered by Google with Gemini Nano, advanced computational photography, and 7 years of Pixel Drops.",
        "default_image_url": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=800&q=80",
        "variants": [
            {
                "name": "128GB Storage, 12GB RAM, Obsidian",
                "sku": "PIXEL9-128-OBS",
                "ram": "12GB",
                "storage": "128GB",
                "color": "Obsidian",
                "mrp": 79999.00,
                "specs": [
                    {"group": "Performance", "name": "Processor", "value": "Google Tensor G4 with Titan M2 security"},
                    {"group": "Display", "name": "Screen Size", "value": "6.3-inch Actua display, 60-120Hz OLED"},
                    {"group": "Camera", "name": "Rear Camera", "value": "50MP Octa PD wide + 48MP Quad PD ultrawide"},
                    {"group": "AI", "name": "Features", "value": "Pixel Studio, Magic Editor, Add Me"},
                ],
                "listings": [
                    {"marketplace_slug": "flipkart", "external_id": "MOBGKP84PIX9", "title": "Google Pixel 9 (Obsidian, 128 GB) (12 GB RAM)", "product_url": "https://www.flipkart.com/google-pixel-9-obsidian-128-gb/p/itmpix9", "current_price": 74999.00, "original_mrp": 79999.00, "availability": "IN_STOCK", "seller_name": "RetailNet", "rating": 4.6, "review_count": 620}
                ]
            }
        ]
    },
    {
        "category_slug": "smartphones",
        "brand_slug": "samsung",
        "name": "Samsung Galaxy A55 5G",
        "slug": "samsung-galaxy-a55-5g",
        "model_number": "SM-A556E",
        "description": "Premium metal frame upper-midranger with Super AMOLED display, IP67 water resistance, and Knox Security.",
        "default_image_url": "https://images.unsplash.com/photo-1580910051074-3eb694886505?auto=format&fit=crop&w=800&q=80",
        "variants": [
            {
                "name": "128GB Storage, 8GB RAM, Awesome Navy",
                "sku": "A55-128-NVY",
                "ram": "8GB",
                "storage": "128GB",
                "color": "Awesome Navy",
                "mrp": 42999.00,
                "specs": [
                    {"group": "Performance", "name": "Processor", "value": "Samsung Exynos 1480 (4nm) with AMD Xclipse 530 GPU"},
                    {"group": "Display", "name": "Screen", "value": "6.6 inches Super AMOLED, 120Hz, Gorilla Glass Victus+"},
                    {"group": "Camera", "name": "Rear Camera", "value": "50MP OIS + 12MP Ultrawide + 5MP Macro"},
                    {"group": "Battery", "name": "Battery", "value": "5000 mAh with 25W Charging"},
                ],
                "listings": [
                    {"marketplace_slug": "amazon", "external_id": "B0CX985A55", "title": "Samsung Galaxy A55 5G (Awesome Navy, 8GB RAM, 128GB Storage)", "product_url": "https://www.amazon.in/dp/B0CX985A55", "current_price": 36999.00, "original_mrp": 42999.00, "availability": "IN_STOCK", "seller_name": "Appario Retail", "rating": 4.4, "review_count": 1890},
                    {"marketplace_slug": "flipkart", "external_id": "MOBGHA55FK128", "title": "SAMSUNG Galaxy A55 5G (Awesome Navy, 128 GB) (8 GB RAM)", "product_url": "https://www.flipkart.com/samsung-galaxy-a55-5g/p/itma55", "current_price": 36499.00, "original_mrp": 42999.00, "availability": "IN_STOCK", "seller_name": "SuperComNet", "rating": 4.4, "review_count": 1240}
                ]
            }
        ]
    },
    {
        "category_slug": "smartphones",
        "brand_slug": "oneplus",
        "name": "OnePlus Nord 4 5G",
        "slug": "oneplus-nord-4-5g",
        "model_number": "CPH2661",
        "description": "All-metal unibody phone powered by Snapdragon 7+ Gen 3 and 5500 mAh battery with 100W charging.",
        "default_image_url": "https://images.unsplash.com/photo-1565849904461-04a58ad377e0?auto=format&fit=crop&w=800&q=80",
        "variants": [
            {
                "name": "128GB Storage, 8GB RAM, Oasis Green",
                "sku": "NORD4-128-GRN",
                "ram": "8GB",
                "storage": "128GB",
                "color": "Oasis Green",
                "mrp": 32999.00,
                "specs": [
                    {"group": "Processor", "name": "Chipset", "value": "Qualcomm Snapdragon 7+ Gen 3 (4nm)"},
                    {"group": "Display", "name": "Screen", "value": "6.74 inches 1.5K AMOLED, 120Hz Ultra HDR"},
                    {"group": "Battery", "name": "Battery", "value": "5500 mAh with 100W SUPERVOOC"},
                    {"group": "Camera", "name": "Primary", "value": "50MP Sony LYT-600 with OIS"},
                ],
                "listings": [
                    {"marketplace_slug": "amazon", "external_id": "B0D77PNORD4", "title": "OnePlus Nord 4 5G (Oasis Green, 8GB RAM, 128GB Storage)", "product_url": "https://www.amazon.in/dp/B0D77PNORD4", "current_price": 28999.00, "original_mrp": 32999.00, "availability": "IN_STOCK", "seller_name": "OnePlus Store", "rating": 4.5, "review_count": 2100}
                ]
            }
        ]
    },

    # ==========================================
    # 2. LAPTOPS
    # ==========================================
    {
        "category_slug": "laptops",
        "brand_slug": "apple",
        "name": "Apple MacBook Air 13-inch (M3)",
        "slug": "apple-macbook-air-13-m3",
        "model_number": "MRXN3HN/A",
        "description": "Supercharged by M3 chip, incredibly thin design, up to 18 hours battery life and Liquid Retina display.",
        "default_image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=800&q=80",
        "variants": [
            {
                "name": "16GB Unified Memory, 256GB SSD, Space Grey",
                "sku": "MBA-M3-16-256-GRY",
                "ram": "16GB",
                "storage": "256GB SSD",
                "color": "Space Grey",
                "mrp": 104900.00,
                "specs": [
                    {"group": "Processor", "name": "CPU", "value": "Apple M3 (8-core CPU, 8-core GPU)"},
                    {"group": "Display", "name": "Screen", "value": "13.6-inch Liquid Retina Display with True Tone"},
                    {"group": "Memory", "name": "Unified Memory", "value": "16GB"},
                    {"group": "Battery", "name": "Battery Life", "value": "Up to 18 hours wireless web"},
                ],
                "listings": [
                    {"marketplace_slug": "amazon", "external_id": "B0CX23M3MBA", "title": "Apple 2024 MacBook Air 13″ Laptop with M3 chip: 16GB Memory, 256GB SSD", "product_url": "https://www.amazon.in/dp/B0CX23M3MBA", "current_price": 99990.00, "original_mrp": 104900.00, "availability": "IN_STOCK", "seller_name": "Appario Retail", "rating": 4.8, "review_count": 1820},
                    {"marketplace_slug": "flipkart", "external_id": "COMSK38MBA13", "title": "Apple MacBook AIR Apple M3 - (16 GB/256 GB SSD) Space Grey", "product_url": "https://www.flipkart.com/apple-macbook-air-m3/p/itmmba13", "current_price": 98990.00, "original_mrp": 104900.00, "availability": "IN_STOCK", "seller_name": "IndiFlashMart", "rating": 4.8, "review_count": 1120}
                ]
            }
        ]
    },
    {
        "category_slug": "laptops",
        "brand_slug": "lenovo",
        "name": "Lenovo Legion Pro 5i Gen 9",
        "slug": "lenovo-legion-pro-5i-gen-9",
        "model_number": "16IRX9",
        "description": "High performance gaming and AI workstation with Intel Core i7-14650HX and NVIDIA RTX 4060 GPU.",
        "default_image_url": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=800&q=80",
        "variants": [
            {
                "name": "16GB RAM, 1TB SSD, RTX 4060 8GB, Eclipse Black",
                "sku": "LEGION-PRO-5I-4060",
                "ram": "16GB DDR5",
                "storage": "1TB NVMe SSD",
                "color": "Eclipse Black",
                "mrp": 164990.00,
                "specs": [
                    {"group": "Processor", "name": "CPU", "value": "Intel Core i7-14650HX (16 Cores, 24 Threads)"},
                    {"group": "Graphics", "name": "GPU", "value": "NVIDIA GeForce RTX 4060 8GB GDDR6 (140W TGP)"},
                    {"group": "Display", "name": "Screen", "value": "16-inch WQXGA (2560x1600) IPS 240Hz 500nits"},
                ],
                "listings": [
                    {"marketplace_slug": "amazon", "external_id": "B0CSKLGN5I", "title": "Lenovo Legion Pro 5 Intel Core i7 14650HX 16\" WQXGA 240Hz Gaming Laptop", "product_url": "https://www.amazon.in/dp/B0CSKLGN5I", "current_price": 139990.00, "original_mrp": 164990.00, "availability": "IN_STOCK", "seller_name": "Lenovo Authorized", "rating": 4.5, "review_count": 420}
                ]
            }
        ]
    },
    {
        "category_slug": "laptops",
        "brand_slug": "asus",
        "name": "ASUS TUF Gaming F15",
        "slug": "asus-tuf-gaming-f15",
        "model_number": "FX506HE-HN382W",
        "description": "Solid entry-level gaming laptop with military-grade durability and dedicated RTX 3050 graphics.",
        "default_image_url": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?auto=format&fit=crop&w=800&q=80",
        "variants": [
            {
                "name": "16GB RAM, 512GB SSD, RTX 3050 4GB, Graphite Black",
                "sku": "TUF-F15-3050-16",
                "ram": "16GB DDR4",
                "storage": "512GB SSD",
                "color": "Graphite Black",
                "mrp": 78990.00,
                "specs": [
                    {"group": "Processor", "name": "CPU", "value": "Intel Core i5-11400H (6 Cores, 12 Threads)"},
                    {"group": "Graphics", "name": "GPU", "value": "NVIDIA GeForce RTX 3050 4GB GDDR6"},
                    {"group": "Display", "name": "Screen", "value": "15.6-inch FHD (1920 x 1080) 144Hz IPS Level"},
                ],
                "listings": [
                    {"marketplace_slug": "amazon", "external_id": "B0C27V76AS", "title": "ASUS TUF Gaming F15, 15.6\"(39.62 cms) FHD 144Hz, Intel Core i5-11400H", "product_url": "https://www.amazon.in/dp/B0C27V76AS", "current_price": 54990.00, "original_mrp": 78990.00, "availability": "IN_STOCK", "seller_name": "Appario Retail", "rating": 4.3, "review_count": 3410},
                    {"marketplace_slug": "flipkart", "external_id": "COMTUFF15FK", "title": "ASUS TUF Gaming F15 Core i5 11th Gen - (16 GB/512 GB SSD/RTX 3050)", "product_url": "https://www.flipkart.com/asus-tuf-f15/p/itmtuf", "current_price": 53990.00, "original_mrp": 78990.00, "availability": "IN_STOCK", "seller_name": "SuperComNet", "rating": 4.4, "review_count": 2980}
                ]
            }
        ]
    },
    {
        "category_slug": "laptops",
        "brand_slug": "dell",
        "name": "Dell Inspiron 15 (Core i5 13th Gen)",
        "slug": "dell-inspiron-15-i5-13th-gen",
        "model_number": "IN3530-I5",
        "description": "Reliable daily productivity laptop with anti-glare display, lift hinge, and fast PCIe SSD.",
        "default_image_url": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?auto=format&fit=crop&w=800&q=80",
        "variants": [
            {
                "name": "16GB RAM, 512GB SSD, Platinum Silver",
                "sku": "DELL-INSP-15-I5",
                "ram": "16GB DDR4",
                "storage": "512GB SSD",
                "color": "Platinum Silver",
                "mrp": 67990.00,
                "specs": [
                    {"group": "Processor", "name": "CPU", "value": "Intel Core i5-1334U (10 Cores, up to 4.60 GHz)"},
                    {"group": "Display", "name": "Screen", "value": "15.6-inch FHD (1920 x 1080) 120Hz WVA Display"},
                    {"group": "Weight", "name": "Weight", "value": "1.65 kg"},
                ],
                "listings": [
                    {"marketplace_slug": "amazon", "external_id": "B0CHWNDELL15", "title": "Dell 15 Thin & Light Laptop, 13th Gen Intel Core i5-1334U Processor", "product_url": "https://www.amazon.in/dp/B0CHWNDELL15", "current_price": 49990.00, "original_mrp": 67990.00, "availability": "IN_STOCK", "seller_name": "Dell Official", "rating": 4.2, "review_count": 890}
                ]
            }
        ]
    },

    # ==========================================
    # 3. TABLETS
    # ==========================================
    {
        "category_slug": "tablets",
        "brand_slug": "apple",
        "name": "Apple iPad 10th Generation",
        "slug": "apple-ipad-10th-generation",
        "model_number": "MPQ03HN/A",
        "description": "All-screen design with 10.9-inch Liquid Retina display, A14 Bionic chip, and USB-C connectivity.",
        "default_image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&w=800&q=80",
        "variants": [
            {
                "name": "64GB Wi-Fi, Blue",
                "sku": "IPAD10-64-BLU",
                "ram": "4GB",
                "storage": "64GB",
                "color": "Blue",
                "mrp": 34900.00,
                "specs": [
                    {"group": "Processor", "name": "Chipset", "value": "A14 Bionic chip with 16-core Neural Engine"},
                    {"group": "Display", "name": "Screen", "value": "10.9-inch Liquid Retina display with True Tone"},
                    {"group": "Camera", "name": "Cameras", "value": "Landscape 12MP Ultra Wide with Center Stage"},
                ],
                "listings": [
                    {"marketplace_slug": "amazon", "external_id": "B0BJMQ8IPAD10", "title": "Apple iPad (10th Generation): with A14 Bionic chip, 10.9-inch Liquid Retina Display", "product_url": "https://www.amazon.in/dp/B0BJMQ8IPAD10", "current_price": 30999.00, "original_mrp": 34900.00, "availability": "IN_STOCK", "seller_name": "Appario Retail", "rating": 4.7, "review_count": 4820},
                    {"marketplace_slug": "flipkart", "external_id": "TABGH83IPAD10", "title": "Apple iPad (10th Gen) 64 GB ROM 10.9 Inch with Wi-Fi Only", "product_url": "https://www.flipkart.com/apple-ipad-10th-gen/p/itmipad10", "current_price": 29999.00, "original_mrp": 34900.00, "availability": "IN_STOCK", "seller_name": "SuperComNet", "rating": 4.7, "review_count": 3400}
                ]
            }
        ]
    },
    {
        "category_slug": "tablets",
        "brand_slug": "oneplus",
        "name": "OnePlus Pad 2",
        "slug": "oneplus-pad-2",
        "model_number": "OPD2404",
        "description": "Ultra-flagship tablet with Snapdragon 8 Gen 3, 3K 144Hz ReadFit display, and 6-speaker stereo audio.",
        "default_image_url": "https://images.unsplash.com/photo-1561154464-82e9adf32764?auto=format&fit=crop&w=800&q=80",
        "variants": [
            {
                "name": "128GB Storage, 8GB RAM, Nimbus Gray",
                "sku": "OPPAD2-128-GRY",
                "ram": "8GB",
                "storage": "128GB",
                "color": "Nimbus Gray",
                "mrp": 42999.00,
                "specs": [
                    {"group": "Processor", "name": "SoC", "value": "Qualcomm Snapdragon 8 Gen 3 (4nm)"},
                    {"group": "Display", "name": "Screen", "value": "12.1-inch 3K (3000x2120) 144Hz 7:5 Display"},
                    {"group": "Battery", "name": "Power", "value": "9510 mAh with 67W SUPERVOOC Fast Charging"},
                ],
                "listings": [
                    {"marketplace_slug": "amazon", "external_id": "B0D77PPAD2", "title": "OnePlus Pad 2 (12.1 Inch LCD Display, 8GB RAM, 128GB Storage)", "product_url": "https://www.amazon.in/dp/B0D77PPAD2", "current_price": 37999.00, "original_mrp": 42999.00, "availability": "IN_STOCK", "seller_name": "OnePlus Store", "rating": 4.6, "review_count": 480}
                ]
            }
        ]
    },

    # ==========================================
    # 4. SMARTWATCHES
    # ==========================================
    {
        "category_slug": "smartwatches",
        "brand_slug": "apple",
        "name": "Apple Watch Series 10 (GPS, 46mm)",
        "slug": "apple-watch-series-10-46mm",
        "model_number": "MWXH3HN/A",
        "description": "Thinnest Apple Watch ever with largest display, sleep apnea notifications, and fast charging.",
        "default_image_url": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?auto=format&fit=crop&w=800&q=80",
        "variants": [
            {
                "name": "46mm, Jet Black",
                "sku": "AWS10-46-BLK",
                "ram": None,
                "storage": "64GB",
                "color": "Jet Black",
                "mrp": 49900.00,
                "specs": [
                    {"group": "Processor", "name": "Chip", "value": "S10 SiP with 64-bit dual-core processor"},
                    {"group": "Display", "name": "Screen", "value": "Wide-angle OLED Always-On Retina display"},
                    {"group": "Health", "name": "Sensors", "value": "ECG app, Blood Oxygen, Depth gauge to 6m, Water temperature"},
                ],
                "listings": [
                    {"marketplace_slug": "amazon", "external_id": "B0DGJ99AW10", "title": "Apple Watch Series 10 (GPS, 46mm) Smartwatch - Jet Black", "product_url": "https://www.amazon.in/dp/B0DGJ99AW10", "current_price": 46900.00, "original_mrp": 49900.00, "availability": "IN_STOCK", "seller_name": "Appario Retail", "rating": 4.7, "review_count": 520}
                ]
            }
        ]
    },
    {
        "category_slug": "smartwatches",
        "brand_slug": "samsung",
        "name": "Samsung Galaxy Watch 7 (Bluetooth, 44mm)",
        "slug": "samsung-galaxy-watch-7-44mm",
        "model_number": "SM-L310N",
        "description": "AI-powered wellness coach with 3nm processor, dual-frequency GPS, and advanced heart health tracking.",
        "default_image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80",
        "variants": [
            {
                "name": "44mm, Green",
                "sku": "GW7-44-GRN",
                "ram": "2GB",
                "storage": "32GB",
                "color": "Green",
                "mrp": 32999.00,
                "specs": [
                    {"group": "Display", "name": "Display", "value": "1.5 inches Super AMOLED Sapphire Crystal"},
                    {"group": "Processor", "name": "Chipset", "value": "Exynos W1000 (3nm, Penta-core)"},
                    {"group": "Sensors", "name": "Health", "value": "BioActive Sensor (ECG, Blood Pressure, Heart Rate)"},
                ],
                "listings": [
                    {"marketplace_slug": "amazon", "external_id": "B0D7B4SGWT7", "title": "Samsung Galaxy Watch7 (Bluetooth, 44mm, Green)", "product_url": "https://www.amazon.in/dp/B0D7B4SGWT7", "current_price": 28999.00, "original_mrp": 32999.00, "availability": "IN_STOCK", "seller_name": "Appario Retail", "rating": 4.5, "review_count": 640}
                ]
            }
        ]
    },

    # ==========================================
    # 5. EARBUDS (TWS)
    # ==========================================
    {
        "category_slug": "earbuds",
        "brand_slug": "apple",
        "name": "Apple AirPods Pro (2nd Gen, USB-C)",
        "slug": "apple-airpods-pro-2-usb-c",
        "model_number": "MTJV3HN/A",
        "description": "Active Noise Cancellation up to 2x more than previous generation, Transparency mode, and Personalized Spatial Audio.",
        "default_image_url": "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?auto=format&fit=crop&w=800&q=80",
        "variants": [
            {
                "name": "Standard, White",
                "sku": "APP2-USBC-WHT",
                "ram": None,
                "storage": None,
                "color": "White",
                "mrp": 24900.00,
                "specs": [
                    {"group": "Audio", "name": "Chip", "value": "Apple H2 Headphone chip, U1 chip in case"},
                    {"group": "Noise Control", "name": "ANC", "value": "Active Noise Cancellation & Adaptive Audio"},
                    {"group": "Battery", "name": "Playtime", "value": "Up to 6 hours listening time, 30 hours with case"},
                ],
                "listings": [
                    {"marketplace_slug": "amazon", "external_id": "B0CHWRXH8B", "title": "Apple AirPods Pro (2nd Generation) with MagSafe Case (USB-C)", "product_url": "https://www.amazon.in/dp/B0CHWRXH8B", "current_price": 20999.00, "original_mrp": 24900.00, "availability": "IN_STOCK", "seller_name": "Appario Retail", "rating": 4.7, "review_count": 4820},
                    {"marketplace_slug": "flipkart", "external_id": "ACCGH83APRO2", "title": "Apple AirPods Pro (2nd generation) with MagSafe Case (USB-C)", "product_url": "https://www.flipkart.com/apple-airpods-pro-2nd-gen-usbc/p/itmpro2", "current_price": 20499.00, "original_mrp": 24900.00, "availability": "IN_STOCK", "seller_name": "SuperComNet", "rating": 4.7, "review_count": 3940}
                ]
            }
        ]
    },
    {
        "category_slug": "earbuds",
        "brand_slug": "oneplus",
        "name": "OnePlus Buds Pro 3",
        "slug": "oneplus-buds-pro-3",
        "model_number": "E512A",
        "description": "Co-created with Dynaudio, featuring dual DACs, 50dB smart adaptive noise cancellation, and LHDC 5.0.",
        "default_image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=800&q=80",
        "variants": [
            {
                "name": "Standard, Midnight Shadow",
                "sku": "OPBP3-SHD",
                "ram": None,
                "storage": None,
                "color": "Midnight Shadow",
                "mrp": 13999.00,
                "specs": [
                    {"group": "Audio", "name": "Drivers", "value": "Dual Drivers (11mm woofer + 6mm tweeter)"},
                    {"group": "ANC", "name": "Cancellation", "value": "Up to 50dB Real-Time Adaptive Noise Cancellation"},
                    {"group": "Battery", "name": "Life", "value": "Up to 43 hours total playback with case"},
                ],
                "listings": [
                    {"marketplace_slug": "amazon", "external_id": "B0DCR9BP3", "title": "OnePlus Buds Pro 3 Bluetooth Truly Wireless in Ear Earbuds", "product_url": "https://www.amazon.in/dp/B0DCR9BP3", "current_price": 11999.00, "original_mrp": 13999.00, "availability": "IN_STOCK", "seller_name": "OnePlus Store", "rating": 4.6, "review_count": 1420}
                ]
            }
        ]
    },

    # ==========================================
    # 6. HEADPHONES (OVER-EAR ANC)
    # ==========================================
    {
        "category_slug": "headphones",
        "brand_slug": "sony",
        "name": "Sony WH-1000XM5 Wireless Headphones",
        "slug": "sony-wh-1000xm5-wireless-headphones",
        "model_number": "WH1000XM5/BM",
        "description": "Industry leading noise canceling with Auto NC Optimizer, 30-hour battery life, and crystal clear calling.",
        "default_image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80",
        "variants": [
            {
                "name": "Standard, Black",
                "sku": "SONY-XM5-BLK",
                "ram": None,
                "storage": None,
                "color": "Black",
                "mrp": 34990.00,
                "specs": [
                    {"group": "Audio", "name": "Noise Cancelling", "value": "Dual processors (V1 + QN1) with 8 microphones"},
                    {"group": "Battery", "name": "Battery Life", "value": "30 hours with ANC on, 40 hours with ANC off"},
                    {"group": "Connectivity", "name": "Bluetooth", "value": "Bluetooth 5.2 with LDAC, Multipoint"},
                ],
                "listings": [
                    {"marketplace_slug": "amazon", "external_id": "B09XS7JWHH", "title": "Sony WH-1000XM5 Wireless Industry Leading Active Noise Cancelling Headphones", "product_url": "https://www.amazon.in/dp/B09XS7JWHH", "current_price": 27990.00, "original_mrp": 34990.00, "availability": "IN_STOCK", "seller_name": "Appario Retail", "rating": 4.6, "review_count": 5210},
                    {"marketplace_slug": "flipkart", "external_id": "ACCGH83SONYXM5", "title": "SONY WH-1000XM5 Bluetooth Headset (Black, On the Ear)", "product_url": "https://www.flipkart.com/sony-wh-1000xm5/p/itmxm5", "current_price": 28490.00, "original_mrp": 34990.00, "availability": "IN_STOCK", "seller_name": "RetailNet", "rating": 4.6, "review_count": 3100}
                ]
            }
        ]
    },
    {
        "category_slug": "headphones",
        "brand_slug": "sony",
        "name": "Sony WH-CH720N Noise Cancelling Headphones",
        "slug": "sony-wh-ch720n-noise-cancelling",
        "model_number": "WHCH720N/B",
        "description": "Best budget ANC headphones in India featuring Integrated Processor V1, 35-hour battery, and lightweight comfort.",
        "default_image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=800&q=80",
        "variants": [
            {
                "name": "Standard, Black",
                "sku": "CH720N-BLK",
                "ram": None,
                "storage": None,
                "color": "Black",
                "mrp": 14990.00,
                "specs": [
                    {"group": "Audio", "name": "ANC", "value": "Dual Noise Sensor technology with V1 Processor"},
                    {"group": "Battery", "name": "Battery", "value": "Up to 35 hours battery life with quick charge"},
                    {"group": "Weight", "name": "Weight", "value": "192g - Sony's lightest overhead wireless ANC headset"},
                ],
                "listings": [
                    {"marketplace_slug": "amazon", "external_id": "B0BT42H2J1", "title": "Sony WH-CH720N, Wireless Over-Ear Active Noise Cancelling Headphones", "product_url": "https://www.amazon.in/dp/B0BT42H2J1", "current_price": 8990.00, "original_mrp": 14990.00, "availability": "IN_STOCK", "seller_name": "Appario Retail", "rating": 4.4, "review_count": 4120}
                ]
            }
        ]
    },

    # ==========================================
    # 7. MONITORS
    # ==========================================
    {
        "category_slug": "monitors",
        "brand_slug": "lg",
        "name": "LG UltraGear 27-inch QHD OLED Gaming Monitor",
        "slug": "lg-ultragear-27-inch-qhd-oled",
        "model_number": "27GS95QE-B",
        "description": "0.03ms response time, 240Hz refresh rate OLED gaming monitor with 98.5% DCI-P3 color gamut.",
        "default_image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=800&q=80",
        "variants": [
            {
                "name": "27-inch, 240Hz, Black",
                "sku": "LG-27GS-OLED",
                "ram": None,
                "storage": None,
                "color": "Black",
                "mrp": 89000.00,
                "specs": [
                    {"group": "Display", "name": "Panel", "value": "27-inch QHD (2560 x 1440) Anti-Glare OLED"},
                    {"group": "Performance", "name": "Speed", "value": "240Hz Refresh Rate, 0.03ms (GtG) response"},
                    {"group": "Sync", "name": "VRR", "value": "NVIDIA G-SYNC Compatible & AMD FreeSync Premium Pro"},
                ],
                "listings": [
                    {"marketplace_slug": "amazon", "external_id": "B0CZDNLG27", "title": "LG UltraGear OLED 27-inch QHD 240Hz Gaming Monitor", "product_url": "https://www.amazon.in/dp/B0CZDNLG27", "current_price": 69999.00, "original_mrp": 89000.00, "availability": "IN_STOCK", "seller_name": "LG India", "rating": 4.7, "review_count": 180}
                ]
            }
        ]
    },

    # ==========================================
    # 8. TELEVISIONS
    # ==========================================
    {
        "category_slug": "televisions",
        "brand_slug": "lg",
        "name": "LG OLED evo C4 55-inch 4K Smart TV",
        "slug": "lg-oled-evo-c4-55-inch",
        "model_number": "OLED55C4PSA",
        "description": "Self-lit OLED pixels with α9 AI Processor Gen7, Dolby Vision, Dolby Atmos, and 144Hz VRR gaming support.",
        "default_image_url": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?auto=format&fit=crop&w=800&q=80",
        "variants": [
            {
                "name": "55-inch, Dark Titan",
                "sku": "LG-C4-55-TITAN",
                "ram": None,
                "storage": None,
                "color": "Dark Titan",
                "mrp": 174990.00,
                "specs": [
                    {"group": "Display", "name": "Panel", "value": "55-inch 4K Self-Lit OLED evo (3840 x 2160)"},
                    {"group": "Refresh Rate", "name": "Hz", "value": "144Hz Native, NVIDIA G-Sync & AMD FreeSync Premium"},
                    {"group": "Processor", "name": "AI Chip", "value": "α9 AI Processor Gen7 4K"},
                ],
                "listings": [
                    {"marketplace_slug": "amazon", "external_id": "B0CZDSLG55C4", "title": "LG 139 cm (55 inches) 4K Ultra HD Smart OLED TV OLED55C4PSA", "product_url": "https://www.amazon.in/dp/B0CZDSLG55C4", "current_price": 129990.00, "original_mrp": 174990.00, "availability": "IN_STOCK", "seller_name": "LG Official", "rating": 4.8, "review_count": 310}
                ]
            }
        ]
    },
    {
        "category_slug": "televisions",
        "brand_slug": "samsung",
        "name": "Samsung Crystal 4K Vivid Pro 55-inch Smart TV",
        "slug": "samsung-crystal-4k-vivid-pro-55",
        "model_number": "UA55DUE77AKXXL",
        "description": "High value 4K UHD smart TV with PurColor, 4K upscaling, SolarCell Remote, and Q-Symphony sound.",
        "default_image_url": "https://images.unsplash.com/photo-1552975084-6e027cd345c2?auto=format&fit=crop&w=800&q=80",
        "variants": [
            {
                "name": "55-inch, Black",
                "sku": "SAM-55-CRYSTAL",
                "ram": None,
                "storage": None,
                "color": "Black",
                "mrp": 68900.00,
                "specs": [
                    {"group": "Display", "name": "Resolution", "value": "4K Ultra HD (3840 x 2160) with HDR 10+"},
                    {"group": "Processor", "name": "Engine", "value": "Crystal Processor 4K"},
                    {"group": "Audio", "name": "Speakers", "value": "20W Output with OTS Lite & Q-Symphony"},
                ],
                "listings": [
                    {"marketplace_slug": "amazon", "external_id": "B0CX585SAM55", "title": "Samsung 138 cm (55 inches) Crystal 4K Vivid Pro Ultra HD Smart LED TV", "product_url": "https://www.amazon.in/dp/B0CX585SAM55", "current_price": 42990.00, "original_mrp": 68900.00, "availability": "IN_STOCK", "seller_name": "Appario Retail", "rating": 4.4, "review_count": 5890},
                    {"marketplace_slug": "flipkart", "external_id": "TVEGH83SAM55C", "title": "SAMSUNG Crystal 4K Vivid Pro 138 cm (55 inch) Ultra HD (4K) LED Smart Tizen TV", "product_url": "https://www.flipkart.com/samsung-crystal-55/p/itmsam55", "current_price": 42490.00, "original_mrp": 68900.00, "availability": "IN_STOCK", "seller_name": "RetailNet", "rating": 4.4, "review_count": 4200}
                ]
            }
        ]
    },

    # ==========================================
    # 9. CAMERAS
    # ==========================================
    {
        "category_slug": "cameras",
        "brand_slug": "sony",
        "name": "Sony Alpha 7 IV Full-Frame Mirrorless Camera",
        "slug": "sony-alpha-7-iv-mirrorless",
        "model_number": "ILCE-7M4",
        "description": "33MP full-frame Exmor R sensor with BIONZ XR engine, 4K 60p 10-bit video, and real-time Eye AF.",
        "default_image_url": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=800&q=80",
        "variants": [
            {
                "name": "Body Only, Black",
                "sku": "A7M4-BODY",
                "ram": None,
                "storage": None,
                "color": "Black",
                "mrp": 242990.00,
                "specs": [
                    {"group": "Sensor", "name": "Sensor", "value": "33.0 MP 35mm full-frame back-illuminated Exmor R CMOS"},
                    {"group": "Video", "name": "Capability", "value": "4K 60p 10-bit 4:2:2 recording, S-Cinetone profile"},
                    {"group": "Autofocus", "name": "AF Points", "value": "759 phase-detection points covering 94% of frame"},
                ],
                "listings": [
                    {"marketplace_slug": "amazon", "external_id": "B09J9F4A7M4", "title": "Sony Alpha 7 IV Full-Frame Hybrid Camera 33MP", "product_url": "https://www.amazon.in/dp/B09J9F4A7M4", "current_price": 204990.00, "original_mrp": 242990.00, "availability": "IN_STOCK", "seller_name": "Sony Authorized", "rating": 4.8, "review_count": 320}
                ]
            }
        ]
    },

    # ==========================================
    # 10. COMPUTER COMPONENTS
    # ==========================================
    {
        "category_slug": "computer-components",
        "brand_slug": "nvidia",
        "name": "NVIDIA GeForce RTX 4070 Super Founders Edition 12GB",
        "slug": "nvidia-geforce-rtx-4070-super-12gb",
        "model_number": "RTX-4070-SUPER-FE",
        "description": "Powered by Ada Lovelace architecture with DLSS 3, 4th gen Tensor cores, and 12GB GDDR6X VRAM.",
        "default_image_url": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&w=800&q=80",
        "variants": [
            {
                "name": "12GB GDDR6X, Founders Edition",
                "sku": "RTX-4070S-FE-12",
                "ram": "12GB GDDR6X",
                "storage": None,
                "color": "Titanium Grey",
                "mrp": 63000.00,
                "specs": [
                    {"group": "Architecture", "name": "GPU", "value": "Ada Lovelace (AD104-350)"},
                    {"group": "CUDA Cores", "name": "Cores", "value": "7168 CUDA Cores"},
                    {"group": "Memory", "name": "VRAM", "value": "12GB GDDR6X (192-bit @ 21 Gbps)"},
                ],
                "listings": [
                    {"marketplace_slug": "amazon", "external_id": "B0CSGVR4070S", "title": "NVIDIA GeForce RTX 4070 Super 12GB Graphics Card", "product_url": "https://www.amazon.in/dp/B0CSGVR4070S", "current_price": 59999.00, "original_mrp": 63000.00, "availability": "IN_STOCK", "seller_name": "ComputeStore India", "rating": 4.8, "review_count": 210}
                ]
            }
        ]
    },
    {
        "category_slug": "computer-components",
        "brand_slug": "amd",
        "name": "AMD Ryzen 7 7800X3D Processor",
        "slug": "amd-ryzen-7-7800x3d",
        "model_number": "100-100000910WOF",
        "description": "The world's undisputed best gaming desktop processor featuring AMD 3D V-Cache technology.",
        "default_image_url": "https://images.unsplash.com/photo-1555680202-c86f0e12f086?auto=format&fit=crop&w=800&q=80",
        "variants": [
            {
                "name": "8 Cores, 16 Threads, 104MB Cache",
                "sku": "RYZEN-7800X3D",
                "ram": None,
                "storage": None,
                "color": "Silver",
                "mrp": 49000.00,
                "specs": [
                    {"group": "Cores", "name": "Architecture", "value": "Zen 4 (8 Cores, 16 Threads)"},
                    {"group": "Cache", "name": "3D V-Cache", "value": "96MB L3 3D V-Cache + 8MB L2 (104MB Total)"},
                    {"group": "Clock", "name": "Frequency", "value": "4.2 GHz Base Clock, up to 5.0 GHz Boost"},
                ],
                "listings": [
                    {"marketplace_slug": "amazon", "external_id": "B0BTZB7F88", "title": "AMD Ryzen 7 7800X3D 8-Core, 16-Thread Desktop Processor", "product_url": "https://www.amazon.in/dp/B0BTZB7F88", "current_price": 38999.00, "original_mrp": 49000.00, "availability": "IN_STOCK", "seller_name": "Appario Retail", "rating": 4.8, "review_count": 1890}
                ]
            }
        ]
    }
]
