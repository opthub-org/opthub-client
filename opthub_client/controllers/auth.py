"""This module contains the functions related to auth command."""

import click


@click.command()
@click.pass_context
def auth(ctx: click.Context) -> None:
    """Sign in."""
