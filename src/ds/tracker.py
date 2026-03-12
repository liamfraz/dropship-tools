import json
from datetime import datetime, timezone
from pathlib import Path

from ds.config import DATA_DIR


class Tracker:
    def __init__(self, data_dir: Path | None = None):
        self.data_dir = data_dir or DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.products_file = self.data_dir / "products.json"
        self.events_file = self.data_dir / "events.json"
        self._ensure_files()

    def _ensure_files(self):
        for f in [self.products_file, self.events_file]:
            if not f.exists():
                f.write_text("[]")

    def _read(self, path: Path) -> list:
        return json.loads(path.read_text())

    def _write(self, path: Path, data: list):
        path.write_text(json.dumps(data, indent=2))

    def add_product(self, name: str, source_cost: float, sell_price: float, platform: str):
        products = self._read(self.products_file)
        products.append({
            "name": name,
            "source_cost": source_cost,
            "sell_price": sell_price,
            "platform": platform,
            "added": datetime.now(timezone.utc).isoformat(),
            "status": "testing",
        })
        self._write(self.products_file, products)

    def list_products(self) -> list[dict]:
        return self._read(self.products_file)

    def _add_event(self, event_type: str, product: str, data: dict):
        events = self._read(self.events_file)
        events.append({
            "type": event_type,
            "product": product,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **data,
        })
        self._write(self.events_file, events)

    def log_sale(self, product: str, units: int, revenue: float):
        self._add_event("sale", product, {"units": units, "revenue": revenue})

    def log_ad_spend(self, product: str, amount: float, platform: str):
        self._add_event("ad_spend", product, {"amount": amount, "ad_platform": platform})

    def get_product_stats(self, product: str) -> dict:
        events = self._read(self.events_file)
        products = self._read(self.products_file)

        product_info = next((p for p in products if p["name"] == product), None)
        if not product_info:
            return {}

        sales = [e for e in events if e["product"] == product and e["type"] == "sale"]
        ad_events = [e for e in events if e["product"] == product and e["type"] == "ad_spend"]

        total_units = sum(s["units"] for s in sales)
        total_revenue = round(sum(s["revenue"] for s in sales), 2)
        total_ad_spend = round(sum(a["amount"] for a in ad_events), 2)
        total_cogs = round(product_info["source_cost"] * total_units, 2)

        roas = round(total_revenue / total_ad_spend, 2) if total_ad_spend > 0 else 0.0
        profit = round(total_revenue - total_cogs - total_ad_spend, 2)

        if total_ad_spend >= product_info["sell_price"] * 3 and total_units == 0:
            verdict = "KILL"
        elif roas >= 2.0:
            verdict = "SCALE"
        elif total_units > 0 and roas >= 1.0:
            verdict = "HOLD"
        elif total_ad_spend > 0 and total_units == 0:
            verdict = "WATCH"
        else:
            verdict = "TESTING"

        return {
            "product": product,
            "total_units": total_units,
            "total_revenue": total_revenue,
            "total_cogs": total_cogs,
            "total_ad_spend": total_ad_spend,
            "profit": profit,
            "roas": roas,
            "verdict": verdict,
        }
