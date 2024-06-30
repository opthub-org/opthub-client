"""This module contains the functions related to auth command."""

import click

from opthub_client.context.credentials import Credentials
from opthub_client.controllers.utils import check_current_version_status
from opthub_client.errors.authentication_error import AuthenticationError


@click.command()
@click.option("--username", "-u", "username", required=True, prompt=True)
@click.option("--password", "-p", "password", prompt=True, hide_input=True)
@click.pass_context
def auth(ctx: click.Context, username: str, password: str) -> None:
    """Sign in."""
    check_current_version_status()
    credentials = Credentials()
    try:
        credentials.cognito_login(username, password)
        click.echo("Successfully signed in.")
    except AuthenticationError as e:
        click.echo(str(e))
    except Exception:
        click.echo("Unexpected error occurred. Please try again later.")
