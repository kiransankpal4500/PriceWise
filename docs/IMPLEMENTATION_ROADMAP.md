# PriceWise Implementation Roadmap

- [x] **Phase 1: Project Inspection & Foundation**
  - [x] Inspect development environment (Node, npm, Python, Git)
  - [x] Verify Gemini API connectivity on free tier (`gemini-3.5-flash-lite`) using official `google-genai` SDK
  - [x] Investigate external repositories (`amazon-mcp`, `ShopIt`, DummyJSON) and document compliance
  - [x] Create project monorepo structure and initial documentation
  - [x] Initialize FastAPI backend with core configuration and health endpoints
  - [x] Initialize Next.js 14 frontend

- [x] **Phase 2: Database & Product Models**
  - [x] Implement SQLAlchemy 2.0 async models for all core entities (Categories, Brands, Products, Variants, Specifications, Marketplaces, Listings, PriceHistory, Watchlists, Alerts, AI Conversations)
  - [x] Configure database session manager & SQLite connection
  - [x] Create Pydantic v2 schemas
  - [x] Build high-fidelity Indian electronics seed dataset across 10 categories
  - [x] Implement database initialization & seeding script

- [x] **Phase 3: Marketplace Discovery & Integration**
  - [x] Build `BaseMarketplaceAdapter` interface and `IntegrationRegistry`
  - [x] Implement Amazon India adapter with respectful rate limiting and state tracking
  - [x] Implement Flipkart adapter
  - [x] Implement DummyJSON demo adapter with `is_demo=True` tagging

- [x] **Phase 4: Product Intelligence**
  - [x] Implement RapidFuzz title normalizer and tokenizer
  - [x] Implement variant detection and extraction (RAM, storage, color, model numbers)
  - [x] Build product matching engine with confidence scoring (`CONFIRMED_MATCH`, `PROBABLE_MATCH`, `REJECTED_MATCH`)

- [x] **Phase 5: Search & Comparison API**
  - [x] Implement `/api/v1/search` with filtering, sorting, and pagination
  - [x] Implement `/api/v1/products/{id}` detail endpoint
  - [x] Implement `/api/v1/compare` endpoint for up to 4 products

- [x] **Phase 6: Recommendation Engine**
  - [x] Implement deterministic scoring algorithm ($S_{\text{price}}$, $S_{\text{spec}}$, $S_{\text{rating}}$, $S_{\text{reviews}}$, $S_{\text{value}}$)
  - [x] Implement category-specific attribute scoring
  - [x] Build natural language explanation generator
  - [x] Implement `/api/v1/recommendations` endpoint

- [x] **Phase 7: Google Gemini AI Shopping Assistant**
  - [x] Implement `GeminiClient` with `gemini-3.5-flash-lite`
  - [x] Define backend tool functions (`search_products`, `get_product_details`, `compare_products`, `get_recommendations`, `get_price_history`)
  - [x] Implement shopping assistant orchestrator with requirement extraction
  - [x] Implement prompt injection guardrails and response validation
  - [x] Implement `/api/v1/assistant/chat` endpoint

- [x] **Phase 8: Price Intelligence & Background Scheduler**
  - [x] Implement price observation recording
  - [x] Implement `/api/v1/products/{id}/prices` historical trend endpoint
  - [x] Implement watchlists and price alerts endpoints
  - [x] Configure APScheduler background worker for price tracking and alert evaluations

- [x] **Phase 9: Review Intelligence & User Accounts**
  - [x] Implement Argon2id password hashing and JWT token generator
  - [x] Implement `/api/v1/auth/register`, `/login`, `/me`
  - [x] Implement review sentiment aggregation

- [x] **Phase 10: Premium Frontend Implementation & End-to-End Verification**
  - [x] Build Next.js App Router UI pages: Home, Search, Product Details, Comparison, AI Assistant, User Dashboard, Deals, Providers
  - [x] Connect frontend to FastAPI backend
  - [x] Execute comprehensive unit and integration test suite (14/14 tests passing)
  - [x] Verify complete user journey acceptance criteria
