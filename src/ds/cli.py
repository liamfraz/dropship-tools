import click
from rich.console import Console
from rich.table import Table

from ds.margin import calculate_margin


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
