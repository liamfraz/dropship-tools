from ds.scout.cj import search_cj_products, CJProduct


def test_cj_product_dataclass():
    p = CJProduct(
        name="Test Product",
        price=8.50,
        shipping_cost=3.00,
        url="https://cjdropshipping.com/test",
        image_url="https://img.example.com/test.jpg",
        category="Home",
        has_us_warehouse=True,
        has_au_warehouse=False,
    )
    assert p.base_cost == 11.50


def test_search_returns_list():
    results = search_cj_products("water bottle", limit=5)
    assert isinstance(results, list)
    assert len(results) <= 5
    # May return empty if CJ is down — that's OK
    if results:
        p = results[0]
        assert isinstance(p, CJProduct)
        assert p.name
        assert p.price >= 0
