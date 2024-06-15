"""This module contains the functions that display the trials to the user."""

import click
from prompt_toolkit.styles import Style

from opthub_client.controllers.utils import get_trial_info_detail, get_trial_info_general
from opthub_client.models.trial import Trial


def display_trial(trial: Trial, is_detail: bool) -> None:
    """Display the trial."""
    if trial is None:
        click.echo("No more solutions to display.")
    else:
        lines = get_trial_info_detail(trial) if is_detail else get_trial_info_general(trial)
        click.echo(lines.rstrip())


def display_trials(trials: list[Trial], is_detail: bool) -> None:
    """Display the trials."""
    if trials is None:
        click.echo("No solutions to display.")
    else:
        lines = ""
        for trial in trials:
            lines += get_trial_info_detail(trial) if is_detail else get_trial_info_general(trial)
        click.echo(lines.rstrip())


def user_interaction_message() -> str:
    """User interaction message for show trials."""
    return '<n style="class:n">n</n>: next solutions, <e style="class:e">e</e>: exit \n'


def user_interaction_message_style() -> Style:
    """Style for user interaction message."""
    style = Style.from_dict(
        {
            "n": "fg:blue bold",
            "e": "fg:red bold",
        },
    )
    return style
