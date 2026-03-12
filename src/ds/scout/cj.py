from dataclasses import dataclass

import httpx
from bs4 import BeautifulSoup


@dataclass
class CJProduct:
    name: str
    price: float
    shipping_cost: float
    url: str
    image_url: str
    category: str
    has_us_warehouse: bool
    has_au_warehouse: bool

    @property
    def base_cost(self) -> float:
        return round(self.price + self.shipping_cost, 2)


def search_cj_products(query: str, limit: int = 10) -> list[CJProduct]:
    """Search CJ Dropshipping catalog via their public search page."""
    url = "https://cjdropshipping.com/search.html"
    params = {"keyword": query}

    try:
        resp = httpx.get(
            url,
            params=params,
            timeout=15,
            follow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        resp.raise_for_status()
    except httpx.HTTPError:
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    products: list[CJProduct] = []

    for card in soup.select(
        ".product-item, .product-card, [class*='product']"
    )[:limit]:
        name_el = card.select_one("[class*='name'], [class*='title'], h3, h4")
        price_el = card.select_one("[class*='price']")
        link_el = card.select_one("a[href]")
        img_el = card.select_one("img")

        if not name_el or not price_el:
            continue

        price_text = price_el.get_text(strip=True).replace("$", "").replace(",", "")
        try:
            price = float(price_text.split("-")[0].strip())
        except (ValueError, IndexError):
            continue

        products.append(
            CJProduct(
                name=name_el.get_text(strip=True),
                price=price,
                shipping_cost=0.0,
                url=link_el["href"] if link_el and link_el.get("href") else "",
                image_url=img_el.get("src", "") if img_el else "",
                category=query,
                has_us_warehouse=False,
                has_au_warehouse=False,
            )
        )

    return products
