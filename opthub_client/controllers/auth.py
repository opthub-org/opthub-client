"""This module contains the functions related to auth command."""

import boto3
import click

from opthub_client.context.credentials import Credentials

CLIENT_ID = "7et20feq5fv89j4k430f7ren7s"
SECRET_HASH = "nrTpTfTDw72mKzN8AD3q813oAH81HpVNFu9+j9g9bLs="


@click.command()
@click.option("--username", "-u", "username", required=True, prompt=True)
@click.option("--password", "-p", "password", prompt=True, hide_input=True)
@click.pass_context
def auth(ctx: click.Context, username: str, password: str) -> None:
    """Sign in."""
    credentials = Credentials()
    credentials.cognito_login(username, password)
