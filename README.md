# Dropship Tools

CLI toolkit that automates the boring parts of dropshipping — product research, margin analysis, AI-generated listings, and performance tracking. All from your terminal.

## Features

### Product Research
- **CJ Search** — Search CJ Dropshipping catalog with warehouse availability (US/AU)
- **Google Trends** — Check trend direction and interest levels for product keywords
- **Scout** — Combined research: trends + product search with automated scoring

### Margin Analysis
- Calculate profit margins with platform fees (TikTok Shop 5%, Shopify 2.9% + $0.30)
- Factor in ad spend per unit
- Get a clear STRONG / OK / SKIP verdict

### AI Content Generation
- **Listings** — Generate optimized product listings for TikTok Shop or Shopify
- **Ad Copy** — Convert TikTok scripts into Facebook/Instagram ad copy
- **Video Scripts** — Generate TikTok video scripts with multiple hook variations

### Performance Tracking
- Track products, log sales, and record ad spend
- Dashboard with revenue, profit, ROAS, and SCALE/HOLD/KILL verdicts

## Installation

```bash
pip install dropship-tools
```

Requires Python 3.12+.

For AI content generation, set your Anthropic API key:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Quick Start

### Check margins on a product

```bash
ds margin --source 8.50 --shipping 3.00 --price 29.99 --platform tiktok
```

```
┌──────────────────────┐
│   Margin Analysis    │
├──────────────────────┤
│ Source Cost    $8.50  │
│ Shipping Cost $3.00  │
│ Sell Price   $29.99  │
│ Platform Fee  $1.50  │
│ Profit/Unit  $17.00  │
│ Markup        2.61x  │
│ ROI          131.1%  │
│ Verdict      STRONG  │
└──────────────────────┘
```

### Search for products

```bash
ds cj "led strip lights" --limit 5
```

### Check Google Trends

```bash
ds trends "posture corrector" "back brace" "neck massager"
```

### Full product scout (trends + search + scoring)

```bash
ds scout "phone holder" "car mount" --limit 10
```

### Generate a TikTok Shop listing

```bash
ds listing "LED Strip Lights" \
  --price 24.99 \
  --platform tiktok \
  --features "16 colors" \
  --features "remote control" \
  --features "USB powered"
```

### Generate TikTok video scripts

```bash
ds scripts "Posture Corrector" \
  --price 29.99 \
  --benefit "fixes slouching" \
  --benefit "invisible under clothes" \
  --hooks 5
```

### Convert to Facebook/Instagram ad copy

```bash
ds adcopy "LED Strip Lights" \
  --script "POV: your room goes from boring to aesthetic in 5 minutes..." \
  --price 24.99 \
  --url "https://shop.example.com/led-strips"
```

### Track product performance

```bash
# Add a product
ds add-product "LED Strip Lights" --source 8.50 --price 24.99 --platform tiktok

# Log sales and ad spend
ds log-sale "LED Strip Lights" --units 12 --revenue 299.88
ds log-spend "LED Strip Lights" --amount 45.00 --platform tiktok

# View dashboard
ds dashboard
```

```
┌──────────────────────────────────────────────────────────────┐
│                 Product Performance Dashboard                │
├─────────────────┬───────┬──────────┬──────────┬──────┬───────┤
│ Product         │ Units │ Revenue  │ Ad Spend │ ROAS │ Verdict│
├─────────────────┼───────┼──────────┼──────────┼──────┼───────┤
│ LED Strip Lights│    12 │  $299.88 │   $45.00 │ 6.66x│ SCALE │
└─────────────────┴───────┴──────────┴──────────┴──────┴───────┘
```

## All Commands

| Command | Description |
|---|---|
| `ds margin` | Calculate profit margins with platform fees |
| `ds cj` | Search CJ Dropshipping catalog |
| `ds trends` | Check Google Trends for keywords |
| `ds scout` | Combined trends + product search with scoring |
| `ds listing` | AI-generate product listings |
| `ds adcopy` | AI-generate Facebook/Instagram ad copy |
| `ds scripts` | AI-generate TikTok video scripts |
| `ds add-product` | Add a product to track |
| `ds log-sale` | Log a sale |
| `ds log-spend` | Log ad spend |
| `ds dashboard` | View performance dashboard |

## Dependencies

- [Click](https://click.palletsprojects.com/) — CLI framework
- [Rich](https://rich.readthedocs.io/) — Terminal formatting
- [Anthropic](https://docs.anthropic.com/) — AI content generation
- [pytrends](https://github.com/GeneralMills/pytrends) — Google Trends data
- [Playwright](https://playwright.dev/python/) — Web scraping
- [BeautifulSoup4](https://beautiful-soup-4.readthedocs.io/) — HTML parsing
- [HTTPX](https://www.python-httpx.org/) — HTTP client

## License

MIT
