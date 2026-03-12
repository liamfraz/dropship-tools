from ds.config import (
    DEFAULT_PLATFORM_FEE_PCT,
    SHOPIFY_PLATFORM_FEE_PCT,
    SHOPIFY_TXN_FEE,
    MIN_MARKUP,
)


def calculate_margin(
    source_cost: float,
    shipping_cost: float,
    sell_price: float,
    platform: str = "tiktok",
    daily_ad_spend: float = 0.0,
    estimated_daily_units: int = 1,
) -> dict:
    base_cost = source_cost + shipping_cost

    if platform == "shopify":
        platform_fee = round(sell_price * SHOPIFY_PLATFORM_FEE_PCT + SHOPIFY_TXN_FEE, 2)
    else:
        platform_fee = round(sell_price * DEFAULT_PLATFORM_FEE_PCT, 2)

    ad_cost_per_unit = (
        round(daily_ad_spend / estimated_daily_units, 2)
        if estimated_daily_units > 0 and daily_ad_spend > 0
        else 0.0
    )

    total_cost = round(base_cost + platform_fee + ad_cost_per_unit, 2)
    profit = round(sell_price - total_cost, 2)
    markup = round(sell_price / base_cost, 2) if base_cost > 0 else 0.0
    roi_pct = round((profit / total_cost) * 100, 2) if total_cost > 0 else 0.0

    if markup < MIN_MARKUP or profit <= 0:
        verdict = "SKIP"
    elif roi_pct >= 40:
        verdict = "STRONG"
    else:
        verdict = "OK"

    return {
        "source_cost": source_cost,
        "shipping_cost": shipping_cost,
        "sell_price": sell_price,
        "base_cost": base_cost,
        "platform": platform,
        "platform_fee": platform_fee,
        "ad_cost_per_unit": ad_cost_per_unit,
        "total_cost_per_unit": total_cost,
        "profit_per_unit": profit,
        "markup": markup,
        "roi_pct": roi_pct,
        "verdict": verdict,
    }
