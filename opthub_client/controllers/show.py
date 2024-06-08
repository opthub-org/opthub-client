"""Group of commands to display trials."""

import click

from opthub_client.controllers.show_trial import show_trial
from opthub_client.controllers.show_trials import show_trials


@click.group()
def show() -> None:
    """Group of commands to display trials."""


show.add_command(show_trials)
show.add_command(show_trial)
