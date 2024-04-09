"""This module contains the functions related to auth command."""

import click


@click.command()
@click.option("--mailaddress", "-m", "mail_address", required=True, prompt=True)
@click.option("--password", "-p", "password", prompt=True, hide_input=True)
@click.pass_context
def auth(ctx: click.Context, mail_address: str, password: str) -> None:
    """Sign in."""
