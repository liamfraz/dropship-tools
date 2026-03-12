from ds.content.ads import build_ad_prompt


def test_build_ad_prompt():
    prompt = build_ad_prompt(
        product_name="LED Strip Lights",
        tiktok_script="POV: you finally made your room look aesthetic...",
        price=28.99,
        landing_url="https://myshop.com/led-lights",
    )
    assert "LED Strip Lights" in prompt
    assert "Facebook" in prompt or "Instagram" in prompt
    assert "28.99" in prompt
