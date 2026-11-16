# PriceWise Security & Compliance Architecture

## 1. Authentication & Password Security
- **Password Hashing**: **Argon2id** via `argon2-cffi` (default memory cost 64MB, 3 iterations, 4 parallelism threads). Plaintext passwords are never stored, logged, or serialized.
- **JWT Authentication**: High-entropy HMAC-SHA256 (`HS256`) signed tokens with strict expiration (60-minute access token, 7-day refresh token).
- **User Ownership Constraints**: All operations on user resources (Watchlists, Price Alerts, AI Conversations) require active token authentication and enforce `user_id == current_user.id` at the repository query level.

---

## 2. LLM / AI Security & Guardrails
- **Zero Exposure**: `GEMINI_API_KEY` is loaded strictly in the backend process from protected environment variables. It is never transmitted to the browser or embedded in client bundles.
- **Controlled Backend Tool Invocation**: Gemini never executes arbitrary code or raw SQL queries. All AI tool executions call tightly typed, pre-validated Pydantic models.
- **Prompt Injection Defense**:
  - User query input is sanitized before inclusion in prompts.
  - External marketplace descriptions are wrapped in `<untrusted_content>` tags and treated as passive data.
  - The model system instructions strictly forbid revealing internal system prompts or departing from the shopping domain.

---

## 3. Scraping & Network Compliance
- **Anti-Bot & CAPTCHA Policy**: Strictly compliant with ethical crawling standards. No CAPTCHA solvers, no proof-of-work evasion, no IP rotation proxies.
- **Graceful Failure**: If a marketplace issues an anti-robot challenge or 503 HTTP status, PriceWise updates the integration status to `RATE_LIMITED` and applies an exponential backoff cooldown rather than re-hammering the target.
- **Demo Data Transparency**: When falling back to mock or demo providers, items are explicitly flagged with `is_demo=True` so users and downstream services know the data is synthetic.
