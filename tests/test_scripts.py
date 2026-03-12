from ds.content.scripts import build_script_prompt


def test_build_script_prompt():
    prompt = build_script_prompt(
        product_name="LED Strip Lights",
        key_benefits=["transforms any room", "easy to install", "remote control"],
        price=28.99,
        num_hooks=5,
    )
    assert "LED Strip Lights" in prompt
    assert "5 different hooks" in prompt
    assert "28.99" in prompt
