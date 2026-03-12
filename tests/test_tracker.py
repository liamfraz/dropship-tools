from ds.tracker import Tracker


def test_add_product(tmp_path):
    tracker = Tracker(data_dir=tmp_path)
    tracker.add_product("LED Lights", source_cost=8.0, sell_price=28.99, platform="tiktok")
    products = tracker.list_products()
    assert len(products) == 1
    assert products[0]["name"] == "LED Lights"


def test_log_sale(tmp_path):
    tracker = Tracker(data_dir=tmp_path)
    tracker.add_product("LED Lights", source_cost=8.0, sell_price=28.99, platform="tiktok")
    tracker.log_sale("LED Lights", units=2, revenue=57.98)
    stats = tracker.get_product_stats("LED Lights")
    assert stats["total_units"] == 2
    assert stats["total_revenue"] == 57.98


def test_log_ad_spend(tmp_path):
    tracker = Tracker(data_dir=tmp_path)
    tracker.add_product("LED Lights", source_cost=8.0, sell_price=28.99, platform="tiktok")
    tracker.log_ad_spend("LED Lights", amount=25.0, platform="tiktok")
    stats = tracker.get_product_stats("LED Lights")
    assert stats["total_ad_spend"] == 25.0


def test_roas_calculation(tmp_path):
    tracker = Tracker(data_dir=tmp_path)
    tracker.add_product("LED Lights", source_cost=8.0, sell_price=28.99, platform="tiktok")
    tracker.log_sale("LED Lights", units=5, revenue=144.95)
    tracker.log_ad_spend("LED Lights", amount=50.0, platform="tiktok")
    stats = tracker.get_product_stats("LED Lights")
    assert stats["roas"] == round(144.95 / 50.0, 2)


def test_kill_verdict(tmp_path):
    tracker = Tracker(data_dir=tmp_path)
    tracker.add_product("Bad Product", source_cost=15.0, sell_price=25.0, platform="tiktok")
    tracker.log_ad_spend("Bad Product", amount=75.0, platform="tiktok")
    stats = tracker.get_product_stats("Bad Product")
    assert stats["verdict"] == "KILL"
