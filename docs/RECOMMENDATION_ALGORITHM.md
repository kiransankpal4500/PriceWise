# PriceWise Recommendation Algorithm Specification

## 1. Algorithm Philosophy
The PriceWise recommendation engine is **deterministic, mathematically explainable, and grounded strictly in verified product data**.

Unlike black-box recommendation algorithms:
- Scores are computed from transparent, verifiable formulas.
- Every recommendation outputs a human-readable "Why this was chosen" and "Potential compromises" rationale.
- Missing specifications are **never** treated as perfect or zero arbitrarily; penalized imputation with transparency is applied.

---

## 2. Core Scoring Formula

For any product variant $i$ within a considered set:

$$\text{Score}(i) = w_{\text{price}} \cdot S_{\text{price}}(i) + w_{\text{spec}} \cdot S_{\text{spec}}(i) + w_{\text{rating}} \cdot S_{\text{rating}}(i) + w_{\text{reviews}} \cdot S_{\text{reviews}}(i) + w_{\text{value}} \cdot S_{\text{value}}(i)$$

Where:
- Default global weights:
  - $w_{\text{price}} = 0.35$ (Budget compliance and competitive pricing)
  - $w_{\text{spec}} = 0.30$ (Category-specific specification benchmarks)
  - $w_{\text{rating}} = 0.20$ (Aggregated customer satisfaction)
  - $w_{\text{reviews}} = 0.10$ (Credibility & review volume)
  - $w_{\text{value}} = 0.05$ (Real price reduction vs historical average / verified MRP)

All sub-scores $S \in [0, 100]$, yielding a normalized final score between 0 and 100.

---

## 3. Sub-Score Formulations

### A. Price Score ($S_{\text{price}}$)
Given user maximum budget $B$ and best available price $P(i)$:
- If $P(i) > B$: $S_{\text{price}}(i) = \max(0, 100 - 200 \times \frac{P(i) - B}{B})$ (Heavy penalty for exceeding budget)
- If $P(i) \le B$: $S_{\text{price}}(i) = 70 + 30 \times (1 - \frac{P(i)}{B})$ (Rewards staying under budget while leaving room for quality)

### B. Rating Score ($S_{\text{rating}}$)
Based on star ratings (typically 1.0 to 5.0):
$$S_{\text{rating}}(i) = \max(0, \min(100, (\text{Rating}(i) - 2.5) \times 40))$$
(A 5.0 star product gets 100; a 3.75 star gets 50; below 2.5 drops to 0).

### C. Review Volume Score ($S_{\text{reviews}}$)
Logarithmic scaling to avoid disproportionately favoring 100,000+ reviews over 2,000 trustworthy reviews:
$$S_{\text{reviews}}(i) = \min(100, \frac{\log_{10}(\text{Count}(i) + 1)}{\log_{10}(10000)} \times 100)$$

### D. Specification Score ($S_{\text{spec}}$)
Category-specific vector dot product. For example:
- **Laptops**: CPU Bench (30%), RAM (20%), Storage SSD (15%), GPU (15%), Battery Wh (10%), Weight/Display (10%)
- **Smartphones**: SoC Benchmark (25%), Primary Camera MP & Sensor (25%), Battery mAh (20%), Fast Charging (15%), RAM/Storage (15%)

---

## 4. Persona & Intent Adapters

When a user specifies a priority:
- **"Best Budget"**: $w_{\text{price}} = 0.55, w_{\text{spec}} = 0.20, w_{\text{rating}} = 0.15, w_{\text{value}} = 0.10$
- **"Best Performance / Gaming"**: $w_{\text{spec}} = 0.55, w_{\text{price}} = 0.20, w_{\text{rating}} = 0.15, w_{\text{reviews}} = 0.10$
- **"Best Camera"**: Category spec weights heavily shifted towards sensor size, OIS, and megapixel quality.
