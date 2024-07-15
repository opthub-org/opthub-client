"""This module contains the functions related to auth command."""

import click

from opthub_client.context.credentials import Credentials
from opthub_client.controllers.utils import check_current_version_status
from opthub_client.errors.authentication_error import AuthenticationError
from opthub_client.errors.cache_io_error import CacheIOError
from opthub_client.errors.fetch_error import FetchError
from opthub_client.errors.query_error import QueryError


@click.command()
@click.option("--username", "-u", "username", required=True, prompt=True)
@click.option("--password", "-p", "password", prompt=True, hide_input=True)
@click.pass_context
def login(ctx: click.Context, username: str, password: str) -> None:  # noqa: ARG001
    """Login."""
    try:
        credentials = Credentials()
        credentials.cognito_login(username, password)
        click.echo(f"Hello {username}. Successfully logged in.")
        check_current_version_status()
    except (CacheIOError, AuthenticationError, QueryError, FetchError) as e:
        e.handler()
