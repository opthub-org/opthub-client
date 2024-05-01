"""This module contains the functions related to auth command."""

import botocore
import click

from opthub_client.context.read_version import get_version
from opthub_client.graphql.version_cli import get_messages


@click.command()
@click.option("--username", "-u", "username", required=True, prompt=True)
@click.option("--password", "-p", "password", prompt=True, hide_input=True)
@click.pass_context
def auth(ctx: click.Context, username: str, password: str) -> None:
    """Sign in."""
    message = get_messages(get_version())
    if message.label == "Error":
        click.echo(click.style(message.label, fg=message.labelColor))
        click.echo(click.style(message.message, fg=message.messageColor))
        return
    credentials = Credentials()
    try:
        credentials.cognito_login(username, password)
        click.echo("Successfully signed in.")
    except botocore.exceptions.ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "NotAuthorizedException":
            # user not exist or incorrect password
            click.echo("Authentication failed. Please verify that your username and password are correct.")
        elif error_code == "TooManyRequestsException":
            click.echo("Too many requests. Please try again later.")
        else:
            click.echo(f"An error occurred: {error_code}")
    except Exception as e:
        # another exception
        click.echo(f"An unexpected error occurred: {e}")
