"""
High-fidelity seed data for PriceWise covering 10 electronics categories in India with INR pricing,
authentic specifications, multiple variants, and marketplace listings for Amazon.in and Flipkart.
"""
import uuid
from datetime import datetime, timedelta, timezone

SEED_CATEGORIES = [
    {"name": "Smartphones", "slug": "smartphones", "description": "Flagship and budget mobile phones", "icon_name": "Smartphone"},
    {"name": "Laptops", "slug": "laptops", "description": "Ultrabooks, gaming and productivity laptops", "icon_name": "Laptop"},
    {"name": "Tablets", "slug": "tablets", "description": "Tablets for productivity and media", "icon_name": "Tablet"},
    {"name": "Smartwatches", "slug": "smartwatches", "description": "Wearables and fitness trackers", "icon_name": "Watch"},
    {"name": "Earbuds", "slug": "earbuds", "description": "True wireless stereo earbuds", "icon_name": "Headphones"},
    {"name": "Headphones", "slug": "headphones", "description": "Over-ear noise cancelling headphones", "icon_name": "Headphones"},
    {"name": "Monitors", "slug": "monitors", "description": "Gaming and professional 4K monitors", "icon_name": "Monitor"},
    {"name": "Televisions", "slug": "televisions", "description": "Smart 4K OLED and QLED TVs", "icon_name": "Tv"},
    {"name": "Cameras", "slug": "cameras", "description": "Mirrorless and DSLR professional cameras", "icon_name": "Camera"},
    {"name": "Computer Components", "slug": "computer-components", "description": "GPUs, processors, RAM and SSDs", "icon_name": "Cpu"},
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
]

SEED_MARKETPLACES = [
    {"name": "Amazon India", "slug": "amazon", "base_url": "https://www.amazon.in", "logo_url": "/marketplaces/amazon.png"},
    {"name": "Flipkart", "slug": "flipkart", "base_url": "https://www.flipkart.com", "logo_url": "/marketplaces/flipkart.png"},
]

# Detailed canonical products catalog
SEED_PRODUCTS = [
    # 1. SMARTPHONE: Samsung Galaxy S25
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
                    {"group": "Camera", "name": "Front Camera", "value": "12MP HDR"},
                    {"group": "Battery", "name": "Battery Capacity", "value": "4000 mAh with 25W Fast Charging"},
                    {"group": "OS", "name": "Operating System", "value": "One UI 7 (Android 15) with 7 years OS updates"},
                ],
                "listings": [
                    {
                        "marketplace_slug": "amazon",
                        "external_id": "B0DXS25AMZ",
                        "title": "Samsung Galaxy S25 5G (Onyx Black, 12GB RAM, 128GB Storage)",
                        "product_url": "https://www.amazon.in/dp/B0DXS25AMZ",
                        "image_url": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?auto=format&fit=crop&w=800&q=80",
                        "current_price": 74999.00,
                        "original_mrp": 79999.00,
                        "availability": "IN_STOCK",
                        "seller_name": "Appario Retail India",
                        "rating": 4.6,
                        "review_count": 1420,
                    },
                    {
                        "marketplace_slug": "flipkart",
                        "external_id": "MOBHX928S25FK",
                        "title": "SAMSUNG Galaxy S25 5G (Onyx Black, 128 GB) (12 GB RAM)",
                        "product_url": "https://www.flipkart.com/samsung-galaxy-s25-5g-onyx-black-128-gb/p/itmdxs25",
                        "image_url": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?auto=format&fit=crop&w=800&q=80",
                        "current_price": 73999.00,
                        "original_mrp": 79999.00,
                        "availability": "IN_STOCK",
                        "seller_name": "TrueCom Retail",
                        "rating": 4.5,
                        "review_count": 980,
                    }
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
                    {"group": "Camera", "name": "Rear Camera", "value": "50MP (Wide, OIS) + 10MP (Telephoto 3x) + 12MP (Ultrawide)"},
                    {"group": "Battery", "name": "Battery Capacity", "value": "4000 mAh with 25W Fast Charging"},
                ],
                "listings": [
                    {
                        "marketplace_slug": "amazon",
                        "external_id": "B0DXS25AMZ2",
                        "title": "Samsung Galaxy S25 5G (Marble Gray, 12GB RAM, 256GB Storage)",
                        "product_url": "https://www.amazon.in/dp/B0DXS25AMZ2",
                        "image_url": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?auto=format&fit=crop&w=800&q=80",
                        "current_price": 79999.00,
                        "original_mrp": 84999.00,
                        "availability": "IN_STOCK",
                        "seller_name": "Appario Retail India",
                        "rating": 4.7,
                        "review_count": 840,
                    }
                ]
            }
        ]
    },
    # 2. SMARTPHONE: Apple iPhone 16
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
                    {"group": "Camera", "name": "Front Camera", "value": "12MP TrueDepth"},
                    {"group": "Battery", "name": "Battery Life", "value": "Up to 22 hours video playback"},
                    {"group": "Special Features", "name": "AI", "value": "Apple Intelligence built-in"},
                ],
                "listings": [
                    {
                        "marketplace_slug": "amazon",
                        "external_id": "B0DGJ68G9H",
                        "title": "Apple iPhone 16 (128 GB) - Ultramarine",
                        "product_url": "https://www.amazon.in/dp/B0DGJ68G9H",
                        "image_url": "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?auto=format&fit=crop&w=800&q=80",
                        "current_price": 76999.00,
                        "original_mrp": 79900.00,
                        "availability": "IN_STOCK",
                        "seller_name": "Amazon Authorized Reseller",
                        "rating": 4.7,
                        "review_count": 3150,
                    },
                    {
                        "marketplace_slug": "flipkart",
                        "external_id": "MOBH8483IPH16",
                        "title": "Apple iPhone 16 (Ultramarine, 128 GB)",
                        "product_url": "https://www.flipkart.com/apple-iphone-16-ultramarine-128-gb/p/itmd83",
                        "image_url": "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?auto=format&fit=crop&w=800&q=80",
                        "current_price": 76499.00,
                        "original_mrp": 79900.00,
                        "availability": "IN_STOCK",
                        "seller_name": "SuperComNet",
                        "rating": 4.7,
                        "review_count": 2890,
                    }
                ]
            }
        ]
    },
    # 3. SMARTPHONE: OnePlus 13
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
                    {"group": "Performance", "name": "Processor", "value": "Qualcomm Snapdragon 8 Elite"},
                    {"group": "Display", "name": "Screen Size", "value": "6.82 inches 2K ProXDR Display, 120Hz LTPO"},
                    {"group": "Camera", "name": "Rear Camera", "value": "50MP Sony LYT-808 + 50MP Periscope + 50MP Ultrawide"},
                    {"group": "Battery", "name": "Battery Capacity", "value": "6000 mAh with 100W SuperVOOC & 50W Wireless"},
                ],
                "listings": [
                    {
                        "marketplace_slug": "amazon",
                        "external_id": "B0DN83KOP13",
                        "title": "OnePlus 13 5G (Midnight Ocean, 12GB RAM, 256GB Storage)",
                        "product_url": "https://www.amazon.in/dp/B0DN83KOP13",
                        "image_url": "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?auto=format&fit=crop&w=800&q=80",
                        "current_price": 64999.00,
                        "original_mrp": 69999.00,
                        "availability": "IN_STOCK",
                        "seller_name": "OnePlus Official Store",
                        "rating": 4.6,
                        "review_count": 890,
                    }
                ]
            }
        ]
    },
    # 4. LAPTOP: Apple MacBook Air M3
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
                    {"group": "Storage", "name": "Drive", "value": "256GB High-Speed SSD"},
                    {"group": "Battery", "name": "Battery Life", "value": "Up to 18 hours wireless web"},
                    {"group": "Weight", "name": "Weight", "value": "1.24 kg"},
                ],
                "listings": [
                    {
                        "marketplace_slug": "amazon",
                        "external_id": "B0CX23M3MBA",
                        "title": "Apple 2024 MacBook Air 13″ Laptop with M3 chip: 13.6-inch Liquid Retina Display, 16GB Unified Memory, 256GB SSD",
                        "product_url": "https://www.amazon.in/dp/B0CX23M3MBA",
                        "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=800&q=80",
                        "current_price": 99990.00,
                        "original_mrp": 104900.00,
                        "availability": "IN_STOCK",
                        "seller_name": "Appario Retail",
                        "rating": 4.8,
                        "review_count": 1820,
                    },
                    {
                        "marketplace_slug": "flipkart",
                        "external_id": "COMSK38MBA13",
                        "title": "Apple MacBook AIR Apple M3 - (16 GB/256 GB SSD/macOS Sonoma) Space Grey",
                        "product_url": "https://www.flipkart.com/apple-macbook-air-m3/p/itmmba13",
                        "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=800&q=80",
                        "current_price": 98990.00,
                        "original_mrp": 104900.00,
                        "availability": "IN_STOCK",
                        "seller_name": "IndiFlashMart",
                        "rating": 4.8,
                        "review_count": 1120,
                    }
                ]
            }
        ]
    },
    # 5. LAPTOP: Lenovo Legion Pro 5i
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
                    {"group": "Display", "name": "Screen", "value": "16-inch WQXGA (2560x1600) IPS 240Hz 500nits 100% sRGB"},
                    {"group": "Cooling", "name": "Thermal System", "value": "Legion Coldfront 5.0 Dual Fan System"},
                ],
                "listings": [
                    {
                        "marketplace_slug": "amazon",
                        "external_id": "B0CSKLGN5I",
                        "title": "Lenovo Legion Pro 5 Intel Core i7 14650HX 16\" (40.64cm) WQXGA 240Hz 500Nits Gaming Laptop",
                        "product_url": "https://www.amazon.in/dp/B0CSKLGN5I",
                        "image_url": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=800&q=80",
                        "current_price": 139990.00,
                        "original_mrp": 164990.00,
                        "availability": "IN_STOCK",
                        "seller_name": "Lenovo Authorized",
                        "rating": 4.5,
                        "review_count": 420,
                    }
                ]
            }
        ]
    },
    # 6. HEADPHONES: Sony WH-1000XM5
    {
        "category_slug": "headphones",
        "brand_slug": "sony",
        "name": "Sony WH-1000XM5 Wireless Headphones",
        "slug": "sony-wh-1000xm5-wireless-headphones",
        "model_number": "WH1000XM5/BM",
        "description": "Industry leading noise canceling with Auto NC Optimizer, 30-hour battery life, and crystal clear hands-free calling.",
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
                    {"group": "Connectivity", "name": "Bluetooth", "value": "Bluetooth 5.2 with LDAC, Multipoint connection"},
                    {"group": "Weight", "name": "Weight", "value": "250 grams"},
                ],
                "listings": [
                    {
                        "marketplace_slug": "amazon",
                        "external_id": "B09XS7JWHH",
                        "title": "Sony WH-1000XM5 Wireless Industry Leading Active Noise Cancelling Headphones",
                        "product_url": "https://www.amazon.in/dp/B09XS7JWHH",
                        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80",
                        "current_price": 27990.00,
                        "original_mrp": 34990.00,
                        "availability": "IN_STOCK",
                        "seller_name": "Appario Retail",
                        "rating": 4.6,
                        "review_count": 5210,
                    },
                    {
                        "marketplace_slug": "flipkart",
                        "external_id": "ACCGH83SONYXM5",
                        "title": "SONY WH-1000XM5 Bluetooth Headset (Black, On the Ear)",
                        "product_url": "https://www.flipkart.com/sony-wh-1000xm5/p/itmxm5",
                        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80",
                        "current_price": 28490.00,
                        "original_mrp": 34990.00,
                        "availability": "IN_STOCK",
                        "seller_name": "RetailNet",
                        "rating": 4.6,
                        "review_count": 3100,
                    }
                ]
            }
        ]
    },
    # 7. SMARTWATCH: Samsung Galaxy Watch 7
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
                    {"group": "Sensors", "name": "Health", "value": "BioActive Sensor (ECG, Blood Pressure, Heart Rate, BIA)"},
                    {"group": "Durability", "name": "Water Resistance", "value": "5ATM + IP68 / MIL-STD-810H"},
                ],
                "listings": [
                    {
                        "marketplace_slug": "amazon",
                        "external_id": "B0D7B4SGWT7",
                        "title": "Samsung Galaxy Watch7 (Bluetooth, 44mm, Green)",
                        "product_url": "https://www.amazon.in/dp/B0D7B4SGWT7",
                        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80",
                        "current_price": 28999.00,
                        "original_mrp": 32999.00,
                        "availability": "IN_STOCK",
                        "seller_name": "Appario Retail",
                        "rating": 4.5,
                        "review_count": 640,
                    }
                ]
            }
        ]
    },
    # 8. EARBUDS: Apple AirPods Pro (2nd Gen, USB-C)
    {
        "category_slug": "earbuds",
        "brand_slug": "apple",
        "name": "Apple AirPods Pro (2nd Generation, MagSafe USB-C)",
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
                    {"group": "Battery", "name": "Playtime", "value": "Up to 6 hours listening time on single charge, 30 hours with case"},
                    {"group": "Protection", "name": "Rating", "value": "IP54 dust, sweat, and water resistant"},
                ],
                "listings": [
                    {
                        "marketplace_slug": "amazon",
                        "external_id": "B0CHWRXH8B",
                        "title": "Apple AirPods Pro (2nd Generation) with MagSafe Case (USB-C)",
                        "product_url": "https://www.amazon.in/dp/B0CHWRXH8B",
                        "image_url": "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?auto=format&fit=crop&w=800&q=80",
                        "current_price": 20999.00,
                        "original_mrp": 24900.00,
                        "availability": "IN_STOCK",
                        "seller_name": "Appario Retail",
                        "rating": 4.7,
                        "review_count": 4820,
                    },
                    {
                        "marketplace_slug": "flipkart",
                        "external_id": "ACCGH83APRO2",
                        "title": "Apple AirPods Pro (2nd generation) with MagSafe Case (USB-C)",
                        "product_url": "https://www.flipkart.com/apple-airpods-pro-2nd-gen-usbc/p/itmpro2",
                        "image_url": "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?auto=format&fit=crop&w=800&q=80",
                        "current_price": 20499.00,
                        "original_mrp": 24900.00,
                        "availability": "IN_STOCK",
                        "seller_name": "SuperComNet",
                        "rating": 4.7,
                        "review_count": 3940,
                    }
                ]
            }
        ]
    },
    # 9. TELEVISIONS: LG OLED evo C4 55-inch 4K Smart TV
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
                    {"group": "Audio", "name": "Sound", "value": "40W 2.2 Channel with Dolby Atmos & AI Sound Pro"},
                ],
                "listings": [
                    {
                        "marketplace_slug": "amazon",
                        "external_id": "B0CZDSLG55C4",
                        "title": "LG 139 cm (55 inches) 4K Ultra HD Smart OLED TV OLED55C4PSA (Dark Titan)",
                        "product_url": "https://www.amazon.in/dp/B0CZDSLG55C4",
                        "image_url": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?auto=format&fit=crop&w=800&q=80",
                        "current_price": 129990.00,
                        "original_mrp": 174990.00,
                        "availability": "IN_STOCK",
                        "seller_name": "LG Official",
                        "rating": 4.8,
                        "review_count": 310,
                    }
                ]
            }
        ]
    },
    # 10. COMPUTER COMPONENTS: NVIDIA GeForce RTX 4070 Super
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
                    {"group": "Power", "name": "TDP", "value": "220W with 16-pin 12VHPWR connector"},
                ],
                "listings": [
                    {
                        "marketplace_slug": "amazon",
                        "external_id": "B0CSGVR4070S",
                        "title": "NVIDIA GeForce RTX 4070 Super 12GB Graphics Card",
                        "product_url": "https://www.amazon.in/dp/B0CSGVR4070S",
                        "image_url": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&w=800&q=80",
                        "current_price": 59999.00,
                        "original_mrp": 63000.00,
                        "availability": "IN_STOCK",
                        "seller_name": "ComputeStore India",
                        "rating": 4.8,
                        "review_count": 210,
                    }
                ]
            }
        ]
    }
]
