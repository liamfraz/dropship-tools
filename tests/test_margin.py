from ds.margin import calculate_margin


def test_basic_margin():
    result = calculate_margin(
        source_cost=8.00,
        shipping_cost=4.00,
        sell_price=32.00,
        platform="tiktok",
        daily_ad_spend=25.00,
        estimated_daily_units=3,
    )
    assert result["base_cost"] == 12.00
    assert result["platform_fee"] == 1.60  # 5% of 32
    assert result["total_cost_per_unit"] > 12.00
    assert result["profit_per_unit"] > 0
    assert result["markup"] > 2.0
    assert "roi_pct" in result
    assert "verdict" in result


def test_margin_too_thin():
    result = calculate_margin(
        source_cost=20.00,
        shipping_cost=5.00,
        sell_price=30.00,
        platform="tiktok",
    )
    assert result["verdict"] == "SKIP"


def test_shopify_fees():
    result = calculate_margin(
        source_cost=8.00,
        shipping_cost=4.00,
        sell_price=32.00,
        platform="shopify",
    )
    assert result["platform_fee"] == round(32.00 * 0.029 + 0.30, 2)


def test_no_ad_spend():
    result = calculate_margin(
        source_cost=8.00,
        shipping_cost=4.00,
        sell_price=32.00,
        platform="tiktok",
    )
    assert result["ad_cost_per_unit"] == 0.0
