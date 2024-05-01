"""This module contains the functions related to auth command."""

import boto3
import click

from opthub_client import __version__
from opthub_client.graphql.version_cli import get_messages


@click.command()
@click.option("--username", "-u", "username", required=True, prompt=True)
@click.option("--password", "-p", "password", prompt=True, hide_input=True)
@click.pass_context
def auth(ctx: click.Context, username: str, password: str) -> None:
    """Sign in."""
    message = get_messages(__version__)
    if message.label == "Error":
        click.echo(click.style(message.label, fg=message.labelColor))
        click.echo(click.style(message.message, fg=message.messageColor))
        return
