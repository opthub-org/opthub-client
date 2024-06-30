"""This module contains the functions related to help command."""

import click

from opthub_client.controllers.auth import auth
from opthub_client.controllers.select import select
from opthub_client.controllers.show import show
from opthub_client.controllers.show_trials import show_trials
from opthub_client.controllers.submit import submit


@click.group(help="OptHub CLI client.")
@click.pass_context
def help(ctx: click.Context) -> None:  # noqa: A001, ARG001
    """Show commands usage."""


help.add_command(show_trials)
help.add_command(select)
help.add_command(submit)
help.add_command(auth)
help.add_command(show)
