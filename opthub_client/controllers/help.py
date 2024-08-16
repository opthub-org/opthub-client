"""This module contains the functions related to help command."""

import click

from opthub_client.controllers.create import create
from opthub_client.controllers.download import download
from opthub_client.controllers.login import login
from opthub_client.controllers.logout import logout
from opthub_client.controllers.select import select
from opthub_client.controllers.show_trial import show_trial
from opthub_client.controllers.show_trials import show_trials
from opthub_client.controllers.submit import submit


@click.group(help="OptHub CLI client.", add_help_option=False)
@click.pass_context
def help(ctx: click.Context) -> None:  # noqa: A001, ARG001
    """Show commands usage."""


help.add_command(show_trials, name="show trials")
help.add_command(show_trial, name="show trial")
help.add_command(select)
help.add_command(submit)
help.add_command(login)
help.add_command(logout)
help.add_command(download)
help.add_command(create)
