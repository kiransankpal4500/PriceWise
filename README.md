# PriceWise — AI-Powered Electronics Price Comparison Platform

**Commercial-grade shopping intelligence for the Indian consumer electronics market (INR ₹).**

PriceWise is a full-stack platform that delivers real-time price comparison across leading Indian marketplaces (Amazon India and Flipkart), deterministic technical specifications comparison, append-only price trend tracking, and grounded conversational advice powered by Google Gemini AI.

---

## 💎 Key Architectural Highlights

1. **₹0 External API Expenditure Policy**:
   - Operates completely on free-tier APIs and ethical open-source integrations.
   - Built with the official `google-genai` Python SDK running on Google Gemini's free tier (`gemini-3.5-flash-lite`).
   - Zero paid proxies, zero paid scraping services, zero paid databases.

2. **Strict Data Grounding & Invariants**:
   - **Variant Isolation**: RapidFuzz and regex attribute parsing guarantee that distinct hardware variants (e.g. 128GB vs 256GB storage) are never merged into false deals.
   - **Append-Only Price Observation**: Historical price data points are never overwritten; every sync appends a timestamped observation.
   - **Synthetic Transparency**: Any demo/fallback data is explicitly flagged and tagged `DEMO DATA` in the UI.

3. **Deterministic Recommendation Engine**:
   - Transparent, mathematical scoring algorithm ($S_{\text{price}}$, $S_{\text{spec}}$, $S_{\text{rating}}$, $S_{\text{reviews}}$, $S_{\text{value}}$).
   - Generates human-readable explanations highlighting why a product ranked #1 and what technical compromises exist.

4. **Security & Ownership**:
   - Password hashing via **Argon2id**.
   - Stateless **JWT authentication** with user-ownership verification for Watchlists, Price Alerts, and Chat Sessions.
   - Prompt-injection defense and input sanitization guardrails.

---

## 🛠️ Technology Stack

- **Frontend**: Next.js 14 (App Router), React 18, TypeScript, Tailwind CSS, Lucide React, Framer Motion, Recharts, Zustand, TanStack Query.
- **Backend**: Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.0 Async, SQLite (PostgreSQL migration-ready), httpx, APScheduler, Argon2id, PyJWT.
- **AI**: Google Gemini API (`google-genai` SDK, `gemini-3.5-flash-lite`).
- **Matching**: RapidFuzz, Python Regex, Pydantic data validation.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+ & npm

### 1. Backend Setup
```bash
cd backend

# Create & activate virtual environment (optional)
# python -m venv venv
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Copy .env.example to .env and configure GEMINI_API_KEY
cp .env.example .env

# Initialize and seed database
python -m app.database.init_db

# Run tests
pytest tests/

# Start FastAPI backend server
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Backend will be available at `http://localhost:8000`
- Interactive OpenAPI Docs: `http://localhost:8000/api/v1/docs`
- Health Endpoint: `http://localhost:8000/api/v1/health`
- Providers Health: `http://localhost:8000/api/v1/health/providers`

### 2. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Or compile production build
npm run build
npm start
```

Frontend will be available at `http://localhost:3000`

---

## 🧪 Testing

PriceWise includes unit and end-to-end integration tests:
```bash
# In backend/
pytest tests/
```
Coverage includes:
- Variant matching accuracy & strict storage/RAM invariants
- Deterministic recommendation scoring & budget penalties
- Complete REST API workflows (Catalog, Details, Search, Compare, Watchlist, Price Alerts, AI Assistant, Auth)

---

## 📚 Project Documentation

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) — Complete modular monolith architecture.
- [DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md) — Entity relationships and table schemas.
- [API_SPECIFICATION.md](docs/API_SPECIFICATION.md) — REST endpoints and schemas.
- [DATA_SOURCES.md](docs/DATA_SOURCES.md) — Data source discovery, licenses, and legal compliance.
- [RECOMMENDATION_ALGORITHM.md](docs/RECOMMENDATION_ALGORITHM.md) — Scoring formulas and weights.
- [SECURITY.md](docs/SECURITY.md) — Authentication, Argon2id, JWT, and LLM guardrails.
- [IMPLEMENTATION_ROADMAP.md](docs/IMPLEMENTATION_ROADMAP.md) — Development phases and deliverables.
- [PROJECT_STATUS.md](docs/PROJECT_STATUS.md) — Completed milestones and verification results.
