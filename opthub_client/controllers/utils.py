"""Util for opthub_client."""

import sys

import click

from opthub_client.context.read_version import get_version_from_file
from opthub_client.graphql.version_cli import get_version_status_messages


def check_current_version_status() -> None:
    """This function gets the version message."""
    messages = get_version_status_messages(get_version_from_file())
    exit_flag = False
    for message in messages:
        if message.label == "Error":
            click.echo(
                click.style(message.label, fg=message.label_color)
                + ": "
                + click.style(
                    message.message,
                    fg=message.message_color,
                ),
            )
            exit_flag = True
        else:
            click.echo(
                click.style(message.label, fg=message.label_color)
                + ": "
                + click.style(
                    message.message,
                    fg=message.message_color,
                ),
            )
    if exit_flag:
        sys.exit(1)