# PriceWise Architecture Documentation

## 1. Overview
PriceWise is a high-performance, AI-powered electronics price comparison and shopping intelligence platform tailored for the Indian consumer electronics market.

The platform follows a **Modular Monolith** architecture:
- Independent frontend (Next.js 14+ App Router, TypeScript, Tailwind CSS, TanStack Query, Zustand)
- Independent backend (FastAPI, Python 3.11+, SQLAlchemy 2.0 Async, Pydantic v2)
- Zero external API expenditure (Free Google Gemini tier with `gemini-3.5-flash-lite`, legal marketplace scraping with respectful rate limiting, and comprehensive built-in catalog data)

```mermaid
flowchart TD
    subgraph Client ["Frontend (Next.js App Router)"]
        UI["UI Pages & Components"]
        Zustand["Zustand Store (Auth & Prefs)"]
        ReactQuery["TanStack Query (Cache & State)"]
    end

    subgraph Backend ["FastAPI Modular Monolith"]
        API["FastAPI REST Router (/api/v1)"]
        AuthMiddleware["JWT & Argon2id Auth"]
        
        subgraph CoreServices ["Core Domain Services"]
            ProductService["Product Catalog Service"]
            SearchService["Search & Filter Engine"]
            MatchingService["RapidFuzz Variant Matching"]
            RecEngine["Deterministic Recommendation Engine"]
            PriceService["Price Observation & Alert Engine"]
            ReviewService["Review Intelligence Service"]
        end

        subgraph AIService ["AI Subsystem"]
            GeminiClient["google-genai Client (Free Tier)"]
            Orchestrator["Shopping Assistant Orchestrator"]
            ToolRegistry["Validated Internal Tools"]
            Guardrails["Prompt Injection & Query Sanitizer"]
        end

        subgraph Adapters ["Marketplace Integrations"]
            AdapterRegistry["Integration Registry"]
            AmazonAdapter["Amazon.in Adapter"]
            FlipkartAdapter["Flipkart Adapter"]
            DemoAdapter["DummyJSON Demo Adapter"]
        end

        subgraph DB ["Database Layer"]
            SQLAlchemy["SQLAlchemy 2.0 Async Engine"]
            SQLite["SQLite / PostgreSQL-ready"]
        end

        subgraph Background ["Scheduler & Workers"]
            APScheduler["APScheduler Async Daemon"]
            PriceWorker["Price Sync & Alert Watcher"]
        end
    end

    UI --> ReactQuery
    ReactQuery --> API
    API --> AuthMiddleware
    AuthMiddleware --> CoreServices
    CoreServices --> DB
    CoreServices --> Adapters
    CoreServices --> AIService
    AIService --> ToolRegistry
    ToolRegistry --> CoreServices
    APScheduler --> PriceWorker
    PriceWorker --> Adapters
    PriceWorker --> PriceService
```

## 2. Component Design & Boundaries

### A. Marketplace Integration Layer (`backend/app/integrations/`)
- Isolated behind `BaseMarketplaceAdapter`
- Standard normalized response format: `MarketplaceProduct` and `MarketplaceOffer`
- Independent state tracker per adapter (`AVAILABLE`, `DEGRADED`, `RATE_LIMITED`, `UNAVAILABLE`)
- Conservative rate limiting and automatic exponential backoff

### B. Product Matching & Deduplication Engine (`backend/app/intelligence/matching/`)
- Tokenizes and cleans product titles (brand removal, regex extraction of RAM/Storage/Color/Model Number)
- Calculates similarity using RapidFuzz (token set ratio, partial ratio)
- Enforces strict variant differentiation: Never conflates different storage/RAM tiers

### C. Recommendation Engine (`backend/app/intelligence/ranking/`)
- Deterministic, explainable scoring model (0-100)
- Configurable weights: Price (35%), Specifications (30%), Rating (20%), Review Volume (10%), Value/Discount (5%)
- Dynamic category-specific attribute weights (e.g. CPU/GPU for laptops, camera/battery for smartphones)

### D. Gemini AI Assistant (`backend/app/ai/`)
- Powered by `google-genai` SDK on `gemini-3.5-flash-lite`
- Controlled tool calling against internal backend services
- Strict guardrails: No SQL execution, no code execution, zero hallucination of fake prices/products
