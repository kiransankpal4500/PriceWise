from typing import List, Optional
from pydantic import BaseModel


class PricePredictionVerdict(BaseModel):
    verdict: str  # STRONG_BUY, BUY, FAIR_PRICE, WAIT
    deal_score: int  # 0 to 100
    badge_label: str  # e.g. "Strong Buy", "Fair Deal", "Wait for Sale"
    color_code: str  # emerald, blue, amber, rose
    rationale: str
    lowest_recorded_price: float
    highest_recorded_price: float
    average_price: float
    savings_vs_peak: float
    expected_savings: float


class PricePredictionEngine:
    @classmethod
    def analyze_price(
        cls,
        current_price: float,
        mrp: float,
        price_history: List[float],
    ) -> PricePredictionVerdict:
        if not price_history:
            price_history = [current_price]

        lowest_p = min(price_history)
        highest_p = max(price_history)
        avg_p = sum(price_history) / len(price_history)

        savings_vs_peak = max(0.0, highest_p - current_price)
        diff_from_lowest = (current_price - lowest_p) / lowest_p if lowest_p > 0 else 0.0

        if diff_from_lowest <= 0.02:
            verdict = "STRONG_BUY"
            deal_score = 96
            badge_label = "Strong Buy"
            color_code = "emerald"
            rationale = (
                f"Currently at ₹{int(current_price):,}, which is within 2% of the all-time lowest recorded price "
                f"(₹{int(lowest_p):,}). You are saving ₹{int(savings_vs_peak):,} compared to its peak price."
            )
            expected_savings = 0.0
        elif diff_from_lowest <= 0.07:
            verdict = "BUY"
            deal_score = 85
            badge_label = "Good Deal"
            color_code = "blue"
            rationale = (
                f"Offered at ₹{int(current_price):,}, which is a competitive price below the historical average "
                f"(₹{int(avg_p):,}). Solid opportunity to buy without waiting."
            )
            expected_savings = round(current_price - lowest_p, 2)
        elif current_price <= avg_p:
            verdict = "FAIR_PRICE"
            deal_score = 70
            badge_label = "Fair Price"
            color_code = "amber"
            rationale = (
                f"Priced at ₹{int(current_price):,}, hovering close to the 90-day average. "
                f"Suitable for immediate purchase if urgently required, though occasional drops occur."
            )
            expected_savings = round(current_price - lowest_p, 2)
        else:
            verdict = "WAIT"
            deal_score = 45
            badge_label = "Wait for Sale"
            color_code = "rose"
            potential_drop = round(current_price - lowest_p, 2)
            rationale = (
                f"Currently near its 90-day high (₹{int(highest_p):,}). "
                f"We recommend setting a price alert—you could save up to ₹{int(potential_drop):,} during upcoming promotional drops."
            )
            expected_savings = potential_drop

        return PricePredictionVerdict(
            verdict=verdict,
            deal_score=deal_score,
            badge_label=badge_label,
            color_code=color_code,
            rationale=rationale,
            lowest_recorded_price=round(lowest_p, 2),
            highest_recorded_price=round(highest_p, 2),
            average_price=round(avg_p, 2),
            savings_vs_peak=round(savings_vs_peak, 2),
            expected_savings=round(expected_savings, 2),
        )
