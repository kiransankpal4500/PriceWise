# PriceWise Database Schema Documentation

The PriceWise database design uses **SQLAlchemy 2.0 Async** with a SQLite local file and is 100% **PostgreSQL-ready** (UUID primary keys, UTC ISO timestamps, Decimal monetary values, foreign key integrity, and explicit indexes).

## Entities & Relationships

```mermaid
erDiagram
    users ||--o{ user_preferences : has
    users ||--o{ watchlists : owns
    users ||--o{ price_alerts : creates
    users ||--o{ ai_conversations : has

    categories ||--o{ products : classifies
    brands ||--o{ products : manufactures

    products ||--o{ product_variants : contains
    product_variants ||--o{ specifications : describes
    product_variants ||--o{ marketplace_listings : offered_as
    product_variants ||--o{ watchlists : saved_in
    product_variants ||--o{ price_alerts : targeted_by

    marketplaces ||--o{ marketplace_listings : hosts
    marketplace_listings ||--o{ price_history : logs
    marketplace_listings ||--o{ reviews : has

    users {
        string id PK
        string email UK
        string hashed_password
        string full_name
        boolean is_active
        boolean is_admin
        datetime created_at
        datetime updated_at
    }

    user_preferences {
        string id PK
        string user_id FK
        decimal default_budget
        json preferred_brands
        json preferred_categories
        json priority_weights
        datetime updated_at
    }

    categories {
        string id PK
        string name UK
        string slug UK
        string description
        string icon_name
    }

    brands {
        string id PK
        string name UK
        string slug UK
        string logo_url
    }

    products {
        string id PK
        string category_id FK
        string brand_id FK
        string name
        string slug UK
        string model_number
        string description
        string default_image_url
        datetime created_at
        datetime updated_at
    }

    product_variants {
        string id PK
        string product_id FK
        string name
        string sku UK
        string ram
        string storage
        string color
        decimal mrp
        datetime created_at
        datetime updated_at
    }

    specifications {
        string id PK
        string variant_id FK
        string spec_group
        string name
        string value
    }

    marketplaces {
        string id PK
        string name UK
        string base_url
        string logo_url
        boolean is_active
    }

    marketplace_listings {
        string id PK
        string variant_id FK
        string marketplace_id FK
        string external_id
        string product_url
        decimal current_price
        decimal original_mrp
        string availability
        string seller_name
        float rating
        integer review_count
        boolean is_demo
        datetime last_scraped_at
    }

    price_history {
        string id PK
        string listing_id FK
        decimal price
        string currency
        string availability
        datetime observed_at
        string source
    }

    watchlists {
        string id PK
        string user_id FK
        string variant_id FK
        datetime added_at
    }

    price_alerts {
        string id PK
        string user_id FK
        string variant_id FK
        decimal target_price
        boolean is_triggered
        datetime triggered_at
        datetime created_at
    }

    ai_conversations {
        string id PK
        string user_id FK
        string title
        json messages
        datetime created_at
        datetime updated_at
    }

    api_sync_logs {
        string id PK
        string provider_name
        string status
        integer items_fetched
        string error_message
        datetime executed_at
    }
```

## Schema Invariants & Design Principles
1. **Append-Only Price Observations**: Old price records in `price_history` are **NEVER overwritten or mutated**. Every sync appends an observation.
2. **Strict Variant Isolation**: `marketplace_listings` map to a specific `product_variants` entity (e.g. 256GB / 12GB RAM), never directly to a generic product entity.
3. **Demo Transparency**: `is_demo` flag is explicitly propagated from listings up to search and details view models.
