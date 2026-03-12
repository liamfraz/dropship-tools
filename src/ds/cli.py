import click


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Dropshipping automation toolkit."""
    pass
