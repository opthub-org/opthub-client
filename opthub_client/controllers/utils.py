"""Util for opthub_client."""

import sys

import click

from opthub_client.context.read_version import get_version
from opthub_client.graphql.version_cli import get_messages


def version_message() -> None:
    """This function gets the version message."""
    message = get_messages(get_version())
    if message.label == "Error":
        click.echo(
            click.style(message.label, fg=message.label_color)
            + ": "
            + click.style(message.message, fg=message.message_color)
        )
        sys.exit()
