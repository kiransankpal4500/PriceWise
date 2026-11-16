# PriceWise Data Sources Documentation

This document records the discovery, technical inspection, licensing, capabilities, and operational constraints for all data sources considered or integrated into PriceWise.

## Policy & Legal Framework
- ₹0 API expenditure strictly enforced.
- No paid proxies, no anti-bot circumvention, no CAPTCHA breaking, no proof-of-work evasion.
- Respect robots.txt, marketplace terms of service, and conservative rate limits.
- Clear data source transparency: All mock or development data is explicitly labeled as `DEMO DATA`.

---

## 1. Amazon India Integration

### Discovery & Research
- **Repository**: `https://github.com/thenabbu/amazon-mcp`
- **License**: MIT License (Confirmed: `external_research/amazon-mcp/LICENSE`)
- **Inspection Findings**:
  - The repository attempts to bypass Akamai interstitial challenges (`_sec/verify?provider=interstitial` with proof-of-work) and form captchas using `curl_cffi` impersonation.
  - **Compliance Decision**: In accordance with our behavioral guidelines and security policy, **PriceWise will NOT incorporate or run any proof-of-work solver or CAPTCHA bypass routines**.
  - **Adapter Architecture**: The Amazon India adapter uses standard respectful HTTP requests (`httpx`) with realistic browser headers and conservative rate-limiting (min 2.0s delay between requests).
  - When Amazon responds with robot-check / 503 / CAPTCHA, the adapter gracefully switches state to `RATE_LIMITED` or `UNAVAILABLE`.
- **Supported Capabilities**:
  - Search keyword queries for products on amazon.in
  - Parsing product title, ASIN, price, MRP, ratings, review count, image URL, and product URL
  - Normalization into canonical PriceWise product schema
- **Price History Consideration**:
  - External price history via pricehistory.app is personal-use only. We maintain an independent append-only price observation store in our SQLite database.

---

## 2. Flipkart Integration

### Discovery & Research
- **Repository**: `https://github.com/bipash25/ShopIt`
- **License**: Unspecified / No explicit root LICENSE file.
- **Inspection Findings**:
  - Uses Flipkart's internal client endpoint: `https://1.rome.api.flipkart.com/api/4/page/fetch` with desktop web user-agent headers.
  - Returns JSON containing widgets, product cards, pricing, and offers.
  - Does not solve CAPTCHAs, but undocumented internal endpoints can change without notice or block requests.
- **Adapter Architecture**:
  - Flipkart adapter (`backend/app/integrations/flipkart/`) runs isolated behind the generic marketplace interface.
  - If Flipkart endpoints block or schema changes, it degrades cleanly to `DEGRADED` or `UNAVAILABLE` without taking down search.

---

## 3. DummyJSON (Development & Test Provider)

- **Official Endpoint**: `https://dummyjson.com/products`
- **License / Terms**: Free public API for testing and prototyping.
- **Role**:
  - Development, automated UI/E2E testing, and fallback.
  - **Critical Rule**: All items from DummyJSON are tagged with `is_demo=True` and clearly badged as `DEMO DATA` in the user interface.

---

## 4. Curated Indian Electronics Catalog (Built-in Verified Seed Data)

- **Role**:
  - High-fidelity canonical product database covering top electronics in India across 10 categories (Smartphones, Laptops, Tablets, Smartwatches, Earbuds, Headphones, Monitors, Televisions, Cameras, Computer Components).
  - Contains real specifications (RAM, storage, processor, battery, camera, display), genuine MRP and street prices in INR, variant structures, and multi-marketplace listing mappings (Amazon.in and Flipkart).
- **Purpose**:
  - Guarantees instant reliable search, deterministic recommendations, and accurate comparison even when external marketplace scrapers encounter rate-limits or network degradation.

---

## 5. Provider Status State Machine

| Status | Meaning | System Behavior |
| :--- | :--- | :--- |
| `AVAILABLE` | Provider responding normally with valid product data | Active in search and price tracking |
| `DEGRADED` | Intermittent errors or partial field extraction | Active with warning logged |
| `RATE_LIMITED` | Marketplace blocked or asked for robot check | Cooldown period triggered; skipped in live search |
| `UNAVAILABLE` | Network failure or endpoint permanently unreachable | Disabled until next health check succeeds |
| `NOT_CONFIGURED` | Missing credentials (for authenticated providers) | Skipped |
| `DISABLED` | Administratively disabled | Excluded from pipeline |
