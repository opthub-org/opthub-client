"""This module contains the functions related to auth command."""

import click

from opthub_client.context.credentials import Credentials
from opthub_client.controllers.utils import check_current_version_status
from opthub_client.errors.authentication_error import AuthenticationError
from opthub_client.errors.cache_io_error import CacheIOError
from opthub_client.errors.fetch_error import FetchError
from opthub_client.errors.query_error import QueryError


@click.command()
@click.pass_context
def logout(ctx: click.Context) -> None:  # noqa: ARG001
    """Logout."""
    try:
        check_current_version_status()
        credentials = Credentials()
        credentials.clear_credentials()
        click.echo("Successfully logged out.")
    except (CacheIOError, AuthenticationError, QueryError, FetchError) as e:
        e.handler()
