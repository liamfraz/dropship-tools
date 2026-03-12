import anthropic


def build_script_prompt(
    product_name: str,
    key_benefits: list[str],
    price: float,
    num_hooks: int = 5,
) -> str:
    benefits_str = "\n".join(f"- {b}" for b in key_benefits)

    return f"""Write {num_hooks} different hooks and script outlines for TikTok videos selling this product.

Product: {product_name}
Price: ${price:.2f}
Key Benefits:
{benefits_str}

For each, provide:
HOOK [number]: [The opening line — must stop the scroll in under 2 seconds]
STYLE: [unboxing / demo / reaction / story / comparison]
SCRIPT: [15-30 second script outline with visual cues in brackets]
CTA: [call to action]

Make them diverse — different angles, tones, and styles. Mix emotional and practical hooks. Keep language natural and casual, not salesy.
"""


def generate_scripts(
    product_name: str,
    key_benefits: list[str],
    price: float,
    num_hooks: int = 5,
) -> str:
    prompt = build_script_prompt(product_name, key_benefits, price, num_hooks)

    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text
