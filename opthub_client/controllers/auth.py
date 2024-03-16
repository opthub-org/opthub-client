import click

@click.command()
@click.pass_context
def signin(ctx,**kwargs):
    """Sign in."""
