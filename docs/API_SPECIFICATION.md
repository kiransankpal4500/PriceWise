# PriceWise REST API Specification

Base URL: `/api/v1`

All requests and responses use JSON and standard HTTP status codes.

---

## 1. Authentication (`/auth`)

### `POST /auth/register`
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePassword123!",
    "full_name": "Sanskriti Rao"
  }
  ```
- **Response**: `201 Created`
  ```json
  {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "Sanskriti Rao",
    "access_token": "jwt_token",
    "token_type": "bearer"
  }
  ```

### `POST /auth/login`
- **Request Body**: `{"email": "...", "password": "..."}`
- **Response**: `200 OK` with `access_token` and user profile.

### `GET /auth/me`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: User profile and preferences.

---

## 2. Products & Catalog (`/products`, `/categories`)

### `GET /categories`
- **Response**: List of categories with slugs, icon names, and product counts.

### `GET /products`
- **Query Params**:
  - `category_slug`: Filter by category (e.g., `smartphones`)
  - `brand_slug`: Filter by brand (e.g., `apple`, `samsung`)
  - `min_price`, `max_price`: INR budget boundaries
  - `sort_by`: `relevance`, `price_asc`, `price_desc`, `rating`, `deal_score`
  - `page`: default 1
  - `page_size`: default 20
- **Response**: Paginated list of canonical products with best current marketplace prices.

### `GET /products/{id_or_slug}`
- **Response**: Full canonical product details, all variants, comprehensive specifications grouped by category, all live marketplace offers, best offer calculation, rating aggregation, and review summary.

---

## 3. Search & Comparison (`/search`, `/compare`)

### `GET /search`
- **Query Params**: `q`, `category`, `brand`, `min_price`, `max_price`, `marketplace`, `sort`, `page`
- **Response**:
  - `query`: sanitized input query
  - `total_results`: count
  - `items`: array of matched products with live marketplace offers and best deal badge
  - `providers_consulted`: status of each marketplace queried (e.g. Amazon, Flipkart, Built-in)

### `POST /compare`
- **Request Body**:
  ```json
  {
    "variant_ids": ["uuid_1", "uuid_2", "uuid_3"]
  }
  ```
- **Response**:
  - Up to 4 products compared side-by-side
  - Aligned specifications table
  - Lowest price across all marketplaces for each
  - Specification differentials highlighted
  - Algorithmic value-for-money verdict

---

## 4. Recommendations (`/recommendations`)

### `POST /recommendations`
- **Request Body**:
  ```json
  {
    "category_slug": "laptops",
    "max_budget": 65000,
    "priorities": {
      "performance": 0.4,
      "battery": 0.3,
      "price": 0.3
    },
    "preferred_brands": ["Lenovo", "Asus", "Apple"]
  }
  ```
- **Response**:
  - Ranked list of products scored 0-100
  - Detailed breakdown of sub-scores (Price, Specs, Rating, Volume, Value)
  - Clear natural language explanation of why the top product won and what compromises it has

---

## 5. Price Tracking & Alerts (`/products/{id}/prices`, `/watchlist`, `/alerts`)

### `GET /products/{variant_id}/prices`
- **Query Params**: `days` (default 90)
- **Response**: Chronological price observations across marketplaces, lowest recorded price, highest recorded price, average price, and current trend.

### `GET /watchlist`, `POST /watchlist`, `DELETE /watchlist/{id}`
- Authenticated user endpoints to track favorite products.

### `GET /alerts`, `POST /alerts`, `DELETE /alerts/{id}`
- Set target price alerts in INR. Triggered automatically by background sync jobs.

---

## 6. AI Shopping Assistant (`/assistant`)

### `POST /assistant/chat`
- **Request Body**:
  ```json
  {
    "conversation_id": "optional-uuid",
    "message": "I have ₹50,000 budget and want a smartphone with top camera and battery."
  }
  ```
- **Response**:
  - `conversation_id`: persistent session ID
  - `response_text`: verified explanation synthesized by Gemini
  - `structured_recommendations`: list of real products fetched via internal tools
  - `requirements_extracted`: `{ "budget": 50000, "priorities": ["camera", "battery"] }`
  - `guardrail_flags`: `{ "injection_detected": false, "hallucination_check": "passed" }`

---

## 7. Health & Monitoring (`/health`, `/health/providers`)

### `GET /health`
- Database connectivity, uptime, version.

### `GET /health/providers`
- Health, rate limit status, and last sync timestamp for Amazon, Flipkart, and Demo providers.
