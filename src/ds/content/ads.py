import anthropic


def build_ad_prompt(
    product_name: str,
    tiktok_script: str,
    price: float,
    landing_url: str,
) -> str:
    return f"""Convert this winning TikTok script into Facebook/Instagram ad copy.

Product: {product_name}
Price: ${price:.2f}
Landing Page: {landing_url}

Original TikTok Script:
{tiktok_script}

Generate 3 variations:

For each:
VARIATION [number]:
HEADLINE: [under 40 chars, attention-grabbing]
PRIMARY TEXT: [ad body, 125 chars max for optimal display, can be longer]
DESCRIPTION: [under 30 chars, appears below headline]
CTA_BUTTON: [Shop Now / Learn More / Get Yours]

Keep the energy of the TikTok script but adapt for Facebook/Instagram ad format. Focus on benefits and social proof angles.
"""


def generate_ad_copy(
    product_name: str,
    tiktok_script: str,
    price: float,
    landing_url: str,
) -> str:
    prompt = build_ad_prompt(product_name, tiktok_script, price, landing_url)

    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text
