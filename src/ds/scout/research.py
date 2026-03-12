from dataclasses import dataclass

from ds.config import MIN_SELL_PRICE, MAX_SELL_PRICE, MAX_SOURCE_COST_PCT
from ds.margin import calculate_margin


@dataclass
class ProductCandidate:
    name: str
    keyword: str
    source_price: float
    shipping_cost: float
    suggested_sell_price: float
    trend_direction: str
    trend_interest: float
    source_url: str


def score_product(candidate: ProductCandidate) -> float:
    """Score a product candidate from 0-100 based on margin, trend, and pricing."""
    score = 50.0

    # Price range check
    if candidate.suggested_sell_price < MIN_SELL_PRICE:
        score -= 20
    elif candidate.suggested_sell_price > MAX_SELL_PRICE:
        score -= 10
    else:
        score += 10

    # Margin verdict
    margin = calculate_margin(
        candidate.source_price,
        candidate.shipping_cost,
        candidate.suggested_sell_price,
        platform="tiktok",
    )
    if margin["verdict"] == "SKIP":
        score -= 25
    elif margin["verdict"] == "STRONG":
        score += 20
    else:
        score += 10

    # Trend direction
    if candidate.trend_direction == "rising":
        score += 15
    elif candidate.trend_direction == "declining":
        score -= 20

    # Trend interest level
    if candidate.trend_interest >= 60:
        score += 10
    elif candidate.trend_interest < 20:
        score -= 10

    # Source cost ratio
    if candidate.source_price > 0 and candidate.suggested_sell_price > 0:
        ratio = candidate.source_price / candidate.suggested_sell_price
        if ratio <= 0.25:
            score += 10
        elif ratio > MAX_SOURCE_COST_PCT:
            score -= 15

    return max(0, min(100, score))


def rank_candidates(
    candidates: list[ProductCandidate],
) -> list[tuple[ProductCandidate, float]]:
    """Score and rank candidates, returning sorted list of (candidate, score) tuples."""
    scored = [(c, score_product(c)) for c in candidates]
    return sorted(scored, key=lambda x: x[1], reverse=True)
