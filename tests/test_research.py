from ds.scout.research import score_product, rank_candidates, ProductCandidate


def test_score_strong_product():
    candidate = ProductCandidate(
        name="LED Strip Lights",
        keyword="led strip lights",
        source_price=6.00,
        shipping_cost=3.00,
        suggested_sell_price=28.00,
        trend_direction="rising",
        trend_interest=75.0,
        source_url="https://example.com",
    )
    score = score_product(candidate)
    assert 0 <= score <= 100
    assert score > 60


def test_score_weak_product():
    candidate = ProductCandidate(
        name="Fidget Spinner",
        keyword="fidget spinner",
        source_price=5.00,
        shipping_cost=2.00,
        suggested_sell_price=15.00,  # Below min price
        trend_direction="declining",
        trend_interest=10.0,
        source_url="https://example.com",
    )
    score = score_product(candidate)
    assert score < 40


def test_score_bounds():
    """Score should always be between 0 and 100."""
    # Worst possible candidate
    worst = ProductCandidate(
        name="Bad Product",
        keyword="bad",
        source_price=50.00,
        shipping_cost=10.00,
        suggested_sell_price=10.00,
        trend_direction="declining",
        trend_interest=5.0,
        source_url="https://example.com",
    )
    score = score_product(worst)
    assert 0 <= score <= 100

    # Best possible candidate
    best = ProductCandidate(
        name="Great Product",
        keyword="great",
        source_price=3.00,
        shipping_cost=1.00,
        suggested_sell_price=30.00,
        trend_direction="rising",
        trend_interest=90.0,
        source_url="https://example.com",
    )
    score = score_product(best)
    assert 0 <= score <= 100


def test_rank_candidates_sorted_descending():
    strong = ProductCandidate(
        name="Strong",
        keyword="strong",
        source_price=5.00,
        shipping_cost=2.00,
        suggested_sell_price=30.00,
        trend_direction="rising",
        trend_interest=80.0,
        source_url="https://example.com",
    )
    weak = ProductCandidate(
        name="Weak",
        keyword="weak",
        source_price=10.00,
        shipping_cost=5.00,
        suggested_sell_price=15.00,
        trend_direction="declining",
        trend_interest=5.0,
        source_url="https://example.com",
    )
    ranked = rank_candidates([weak, strong])
    assert ranked[0][0].name == "Strong"
    assert ranked[0][1] > ranked[1][1]
