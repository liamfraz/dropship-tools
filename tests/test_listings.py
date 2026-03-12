from ds.content.listings import build_listing_prompt


def test_build_listing_prompt():
    prompt = build_listing_prompt(
        product_name="LED Strip Lights 5m RGB",
        category="Home Decor",
        key_features=["5 meters", "RGB color changing", "remote control", "USB powered"],
        price=28.99,
        platform="tiktok",
    )
    assert "LED Strip Lights" in prompt
    assert "TikTok" in prompt
    assert "28.99" in prompt


def test_build_listing_prompt_shopify():
    prompt = build_listing_prompt(
        product_name="LED Strip Lights",
        category="Home",
        key_features=["RGB"],
        price=28.99,
        platform="shopify",
    )
    assert "Shopify" in prompt
    assert "SEO" in prompt
