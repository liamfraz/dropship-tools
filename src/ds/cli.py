import click
from rich.console import Console
from rich.table import Table

from ds.config import TARGET_MARKUP
from ds.margin import calculate_margin
from ds.scout.cj import search_cj_products
from ds.scout.research import ProductCandidate, rank_candidates
from ds.scout.trends import check_trend, check_trends_batch
from ds.content.ads import generate_ad_copy
from ds.content.listings import generate_listing
from ds.content.scripts import generate_scripts


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


@cli.command()
@click.argument("keywords", nargs=-1, required=True)
@click.option("--limit", type=int, default=15, help="Max products to display")
def scout(keywords, limit):
    """Combined product scout: trends + CJ search with scoring."""
    console = Console()
    console.print(f"[cyan]Scouting {len(keywords)} keyword(s)...[/]")

    candidates: list[ProductCandidate] = []

    for keyword in keywords:
        console.print(f"  [dim]Checking trends for '{keyword}'...[/]")
        trend = check_trend(keyword)

        console.print(f"  [dim]Searching CJ for '{keyword}'...[/]")
        products = search_cj_products(keyword, limit=limit)

        for p in products:
            suggested_sell = round(p.base_cost * TARGET_MARKUP, 2)
            candidates.append(
                ProductCandidate(
                    name=p.name,
                    keyword=keyword,
                    source_price=p.price,
                    shipping_cost=p.shipping_cost,
                    suggested_sell_price=suggested_sell,
                    trend_direction=trend["trend_direction"],
                    trend_interest=float(trend["avg_interest"]),
                    source_url=p.url,
                )
            )

    if not candidates:
        console.print("[yellow]No products found for any keyword.[/]")
        return

    ranked = rank_candidates(candidates)[:limit]

    table = Table(title="Product Scout Results", border_style="blue")
    table.add_column("Score", justify="right", width=6)
    table.add_column("Name", style="cyan", max_width=40)
    table.add_column("Source $", justify="right")
    table.add_column("Sell $", justify="right")
    table.add_column("Trend", justify="center")
    table.add_column("Keyword", style="dim")

    for candidate, score in ranked:
        if score >= 60:
            score_style = "bold green"
        elif score >= 40:
            score_style = "bold yellow"
        else:
            score_style = "bold red"

        direction_style = {
            "rising": "green",
            "stable": "yellow",
            "declining": "red",
            "no_data": "dim",
        }.get(candidate.trend_direction, "")

        table.add_row(
            f"[{score_style}]{score:.0f}[/]",
            candidate.name,
            f"${candidate.source_price:.2f}",
            f"${candidate.suggested_sell_price:.2f}",
            f"[{direction_style}]{candidate.trend_direction}[/]",
            candidate.keyword,
        )

    console.print(table)


@cli.command("add-product")
@click.argument("name")
@click.option("--source", required=True, type=float, help="Source/product cost")
@click.option("--price", required=True, type=float, help="Sell price")
@click.option(
    "--platform",
    type=click.Choice(["tiktok", "shopify"], case_sensitive=False),
    default="tiktok",
    help="Sales platform",
)
def add_product(name, source, price, platform):
    """Add a product to track."""
    tracker = Tracker()
    tracker.add_product(name, source_cost=source, sell_price=price, platform=platform)
    console = Console()
    console.print(f"[green]Added product:[/] {name} (${source:.2f} -> ${price:.2f}, {platform})")


@cli.command("log-sale")
@click.argument("product")
@click.option("--units", required=True, type=int, help="Number of units sold")
@click.option("--revenue", required=True, type=float, help="Total revenue")
def log_sale(product, units, revenue):
    """Log a sale for a tracked product."""
    tracker = Tracker()
    tracker.log_sale(product, units=units, revenue=revenue)
    console = Console()
    console.print(f"[green]Logged sale:[/] {product} — {units} units, ${revenue:.2f}")


@cli.command("log-spend")
@click.argument("product")
@click.option("--amount", required=True, type=float, help="Ad spend amount")
@click.option(
    "--platform",
    type=click.Choice(["tiktok", "facebook"], case_sensitive=False),
    default="tiktok",
    help="Ad platform",
)
def log_spend(product, amount, platform):
    """Log ad spend for a tracked product."""
    tracker = Tracker()
    tracker.log_ad_spend(product, amount=amount, platform=platform)
    console = Console()
    console.print(f"[green]Logged ad spend:[/] {product} — ${amount:.2f} on {platform}")


@cli.command()
def dashboard():
    """Show performance dashboard for all tracked products."""
    tracker = Tracker()
    products = tracker.list_products()
    console = Console()

    if not products:
        console.print("[yellow]No products tracked yet. Use 'ds add-product' to start.[/]")
        return

    verdict_color = {
        "SCALE": "bold green",
        "HOLD": "bold yellow",
        "WATCH": "bold cyan",
        "KILL": "bold red",
        "TESTING": "dim",
    }

    table = Table(title="Product Performance Dashboard", border_style="blue")
    table.add_column("Product", style="cyan")
    table.add_column("Units", justify="right")
    table.add_column("Revenue", justify="right")
    table.add_column("Ad Spend", justify="right")
    table.add_column("Profit", justify="right")
    table.add_column("ROAS", justify="right")
    table.add_column("Verdict", justify="center")

    for p in products:
        stats = tracker.get_product_stats(p["name"])
        if not stats:
            continue

        profit_style = "green" if stats["profit"] >= 0 else "red"
        verdict = stats["verdict"]
        v_style = verdict_color.get(verdict, "")

        table.add_row(
            stats["product"],
            str(stats["total_units"]),
            f"${stats['total_revenue']:.2f}",
            f"${stats['total_ad_spend']:.2f}",
            f"[{profit_style}]${stats['profit']:.2f}[/]",
            f"{stats['roas']:.2f}x",
            f"[{v_style}]{verdict}[/]",
        )

    console.print(table)


@cli.command()
@click.argument("product_name")
@click.option("--category", default="General", help="Product category")
@click.option("--features", multiple=True, help="Key product features (repeatable)")
@click.option("--price", required=True, type=float, help="Product price")
@click.option(
    "--platform",
    type=click.Choice(["tiktok", "shopify"], case_sensitive=False),
    default="tiktok",
    help="Listing platform",
)
def listing(product_name, category, features, price, platform):
    """Generate AI product listing for TikTok Shop or Shopify."""
    console = Console()
    console.print(f"[cyan]Generating {platform} listing for:[/] {product_name}")

    result = generate_listing(
        product_name=product_name,
        category=category,
        key_features=list(features) if features else ["Quality product"],
        price=price,
        platform=platform,
    )

    if "title" in result:
        console.print(f"\n[bold green]TITLE:[/] {result['title']}")
    if "description" in result:
        console.print(f"\n[bold green]DESCRIPTION:[/] {result['description']}")
    if "tags" in result:
        console.print(f"\n[bold green]TAGS:[/] {', '.join(result['tags'])}")

    if not any(k in result for k in ("title", "description", "tags")):
        console.print(f"\n[yellow]Raw output:[/]\n{result['raw']}")


@cli.command()
@click.argument("product_name")
@click.option("--script", required=True, type=str, help="TikTok script text to convert")
@click.option("--price", required=True, type=float, help="Product price")
@click.option("--url", required=True, type=str, help="Landing page URL")
def adcopy(product_name, script, price, url):
    """Convert a TikTok script into Facebook/Instagram ad copy."""
    console = Console()
    console.print(f"[cyan]Generating ad copy for:[/] {product_name}")

    result = generate_ad_copy(
        product_name=product_name,
        tiktok_script=script,
        price=price,
        landing_url=url,
    )

    console.print(f"\n{result}")


@cli.command()
@click.argument("product_name")
@click.option("--benefit", multiple=True, help="Key product benefit (repeatable)")
@click.option("--price", required=True, type=float, help="Product price")
@click.option("--hooks", default=5, type=int, help="Number of hook variations")
def scripts(product_name, benefit, price, hooks):
    """Generate TikTok video scripts with multiple hook variations."""
    console = Console()
    console.print(f"[cyan]Generating {hooks} script hooks for:[/] {product_name}")

    benefits = list(benefit) if benefit else ["Great product"]
    result = generate_scripts(
        product_name=product_name,
        key_benefits=benefits,
        price=price,
        num_hooks=hooks,
    )

    console.print()
    console.print(result)
