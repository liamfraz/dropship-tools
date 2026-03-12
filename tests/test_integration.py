"""Integration test — verifies the full workflow hangs together.
Does NOT call external APIs (trends, Claude). Tests the local pipeline only."""

from ds.margin import calculate_margin
from ds.scout.research import ProductCandidate, score_product, rank_candidates
from ds.tracker import Tracker


def test_full_local_workflow(tmp_path):
    # 1. Score a product candidate
    candidate = ProductCandidate(
        name="LED Strip Lights 5m",
        keyword="led strip lights",
        source_price=6.00,
        shipping_cost=3.00,
        suggested_sell_price=28.00,
        trend_direction="rising",
        trend_interest=72.0,
        source_url="https://cjdropshipping.com/led-lights",
    )
    score = score_product(candidate)
    assert score > 50

    # 2. Calculate margin
    margin = calculate_margin(
        source_cost=6.00,
        shipping_cost=3.00,
        sell_price=28.00,
        platform="tiktok",
        daily_ad_spend=25.00,
        estimated_daily_units=3,
    )
    assert margin["verdict"] in ("OK", "STRONG")
    assert margin["profit_per_unit"] > 0

    # 3. Track the product
    tracker = Tracker(data_dir=tmp_path)
    tracker.add_product("LED Strip Lights 5m", source_cost=6.00, sell_price=28.00, platform="tiktok")

    # 4. Log some activity
    tracker.log_sale("LED Strip Lights 5m", units=3, revenue=84.00)
    tracker.log_ad_spend("LED Strip Lights 5m", amount=25.00, platform="tiktok")

    # 5. Check dashboard stats
    stats = tracker.get_product_stats("LED Strip Lights 5m")
    assert stats["total_units"] == 3
    assert stats["total_revenue"] == 84.00
    assert stats["roas"] == round(84.00 / 25.00, 2)
    assert stats["verdict"] == "SCALE"  # ROAS > 2x
