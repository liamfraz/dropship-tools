from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent / "data"
PRODUCTS_FILE = DATA_DIR / "products.json"
PERFORMANCE_FILE = DATA_DIR / "performance.json"

# Margin defaults
DEFAULT_PLATFORM_FEE_PCT = 0.05  # TikTok Shop ~5%
SHOPIFY_PLATFORM_FEE_PCT = 0.029  # + $0.30 per txn
SHOPIFY_TXN_FEE = 0.30

# Selection criteria
MIN_SELL_PRICE = 20.0
MAX_SELL_PRICE = 60.0
MAX_SOURCE_COST_PCT = 0.40  # Source must be under 40% of sell price
MIN_MARKUP = 2.5
TARGET_MARKUP = 3.0
