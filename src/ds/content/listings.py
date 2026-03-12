import anthropic


def build_listing_prompt(
    product_name: str,
    category: str,
    key_features: list[str],
    price: float,
    platform: str = "tiktok",
) -> str:
    platform_guidance = {
        "tiktok": "TikTok Shop listing. Use casual, engaging tone. Emoji-friendly. Short punchy sentences. Max 500 chars for description. Include relevant hashtags.",
        "shopify": "Shopify product page. Professional but friendly. Benefit-focused bullet points. SEO-optimized title and description. Include meta description.",
    }

    features_str = "\n".join(f"- {f}" for f in key_features)

    return f"""Write a {platform_guidance.get(platform, platform_guidance['tiktok'])}

Product: {product_name}
Category: {category}
Price: ${price:.2f}
Key Features:
{features_str}

Output format:
TITLE: [product title optimized for {platform} search]
DESCRIPTION: [product description]
TAGS: [comma-separated tags/hashtags]
"""


def generate_listing(
    product_name: str,
    category: str,
    key_features: list[str],
    price: float,
    platform: str = "tiktok",
) -> dict:
    prompt = build_listing_prompt(product_name, category, key_features, price, platform)

    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    text = message.content[0].text
    result = {"raw": text, "platform": platform}

    for line in text.split("\n"):
        if line.startswith("TITLE:"):
            result["title"] = line.replace("TITLE:", "").strip()
        elif line.startswith("DESCRIPTION:"):
            result["description"] = line.replace("DESCRIPTION:", "").strip()
        elif line.startswith("TAGS:"):
            result["tags"] = [t.strip() for t in line.replace("TAGS:", "").split(",")]

    return result
