"""This module contains the functions related to auth command."""

import click

from opthub_client.context.credentials import Credentials
from opthub_client.controllers.utils import check_current_version_status
from opthub_client.errors.authentication_error import AuthenticationError
from opthub_client.errors.cache_io_error import CacheIOError
from opthub_client.errors.graphql_error import GraphQLError
from opthub_client.errors.query_error import QueryError


@click.command()
@click.option("--username", "-u", "username", required=True, prompt=True)
@click.option("--password", "-p", "password", prompt=True, hide_input=True)
@click.pass_context
def auth(ctx: click.Context, username: str, password: str) -> None:
    """Sign in."""
    try:
        check_current_version_status()
        credentials = Credentials()
        credentials.cognito_login(username, password)
        click.echo("Successfully signed in.")
    except (CacheIOError, AuthenticationError, QueryError, GraphQLError) as e:
        e.error_handler()
    except Exception:
        click.echo("Unexpected error occurred. Please try again later.")
