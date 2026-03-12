import click
from rich.console import Console
from rich.table import Table

from ds.margin import calculate_margin
from ds.scout.cj import search_cj_products
from ds.scout.trends import check_trends_batch


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Dropshipping automation toolkit."""
    pass


@cli.command()
@click.option("--source", required=True, type=float, help="Source/product cost")
@click.option("--shipping", required=True, type=float, help="Shipping cost")
@click.option("--price", required=True, type=float, help="Sell price")
@click.option(
    "--platform",
    type=click.Choice(["tiktok", "shopify"], case_sensitive=False),
    default="tiktok",
    help="Sales platform",
)
@click.option("--ad-spend", type=float, default=0.0, help="Daily ad spend")
@click.option("--daily-units", type=int, default=1, help="Estimated daily units sold")
def margin(source, shipping, price, platform, ad_spend, daily_units):
    """Calculate profit margins for a product."""
    result = calculate_margin(
        source_cost=source,
        shipping_cost=shipping,
        sell_price=price,
        platform=platform,
        daily_ad_spend=ad_spend,
        estimated_daily_units=daily_units,
    )

    console = Console()

    verdict_color = {
        "STRONG": "bold green",
        "OK": "bold yellow",
        "SKIP": "bold red",
    }

    table = Table(title="Margin Analysis", show_header=False, border_style="blue")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right")

    table.add_row("Source Cost", f"${result['source_cost']:.2f}")
    table.add_row("Shipping Cost", f"${result['shipping_cost']:.2f}")
    table.add_row("Base Cost", f"${result['base_cost']:.2f}")
    table.add_row("Sell Price", f"${result['sell_price']:.2f}")
    table.add_row("Platform", result["platform"])
    table.add_row("Platform Fee", f"${result['platform_fee']:.2f}")
    table.add_row("Ad Cost/Unit", f"${result['ad_cost_per_unit']:.2f}")
    table.add_row("Total Cost/Unit", f"${result['total_cost_per_unit']:.2f}")
    table.add_row("Profit/Unit", f"${result['profit_per_unit']:.2f}")
    table.add_row("Markup", f"{result['markup']:.2f}x")
    table.add_row("ROI", f"{result['roi_pct']:.1f}%")
    table.add_row(
        "Verdict",
        f"[{verdict_color.get(result['verdict'], '')}]{result['verdict']}[/]",
    )

    console.print(table)


@cli.command()
@click.argument("query")
@click.option("--limit", type=int, default=10, help="Max number of results")
def cj(query, limit):
    """Search CJ Dropshipping for products."""
    console = Console()
    console.print(f"[cyan]Searching CJ Dropshipping for:[/] {query}")

    results = search_cj_products(query, limit=limit)

    if not results:
        console.print("[yellow]No results found (CJ may be blocking or no matches).[/]")
        return

    table = Table(title="CJ Dropshipping Results", border_style="blue")
    table.add_column("Name", style="cyan", max_width=40)
    table.add_column("Price", justify="right")
    table.add_column("US WH", justify="center")
    table.add_column("AU WH", justify="center")

    for p in results:
        table.add_row(
            p.name,
            f"${p.base_cost:.2f}",
            "[green]Yes[/]" if p.has_us_warehouse else "[red]No[/]",
            "[green]Yes[/]" if p.has_au_warehouse else "[red]No[/]",
        )

    console.print(table)


@cli.command()
@click.argument("keywords", nargs=-1, required=True)
@click.option(
    "--timeframe",
    default="today 3-m",
    help="Trends timeframe (default: today 3-m)",
)
def trends(keywords, timeframe):
    """Check Google Trends interest for product keywords."""
    console = Console()
    console.print(f"[cyan]Checking Google Trends for {len(keywords)} keyword(s)...[/]")

    results = check_trends_batch(list(keywords), timeframe=timeframe)

    direction_style = {
        "rising": "bold green",
        "stable": "bold yellow",
        "declining": "bold red",
        "no_data": "dim",
    }

    table = Table(title="Google Trends Analysis", border_style="blue")
    table.add_column("Keyword", style="cyan")
    table.add_column("Direction", justify="center")
    table.add_column("Avg Interest", justify="right")
    table.add_column("Recent Interest", justify="right")

    for r in results:
        direction = r["trend_direction"]
        style = direction_style.get(direction, "")
        table.add_row(
            r["keyword"],
            f"[{style}]{direction}[/]",
            str(r["avg_interest"]),
            str(r["recent_interest"]),
        )

    console.print(table)
