import click


@click.command()
@click.pass_context
def auth(ctx: click.Context) -> None:
    """Sign in."""
