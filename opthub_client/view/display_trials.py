"""This module contains the functions that display the trials to the user."""

import click
from prompt_toolkit.styles import Style

from opthub_client.models.trial import Trial


def display_trial(trial: Trial | None, is_detail: bool) -> None:
    """Display the trial."""
    if trial is None:
        click.echo("No more solutions to display.")
    else:
        lines = get_trial_info_detail(trial) if is_detail else get_trial_info_general(trial)
        click.echo(lines.rstrip())


def display_trials(trials: list[Trial], is_detail: bool) -> None:
    """Display the trials."""
    if len(trials) == 0:
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


def get_trial_info_general(trial: Trial) -> str:
    """Display the general information of a trial.

    Args:
        trial (Trial): The trial to display.

    Returns:
        str: The general information of the trial.
    """
    lines = (
        f"Trial No: {trial['trialNo']}, status: {trial['status']}, Score: {trial['score']['score']}\n"
        if trial["score"]
        else f"Trial No: {trial['trialNo']}, status: {trial['status']}\n"
    )

    return lines


def get_trial_info_detail(trial: Trial) -> str:
    """Display the general information of a trial.

    Args:
        trial (Trial): The trial to display.

    Returns:
        str: The general information of the trial.
    """
    lines = ""
    lines += "Trial No: " + str(trial["trialNo"]) + "\n"
    lines += "status: " + str(trial["status"]) + "\n"
    lines += "Solution: " + str(trial["solution"]["variable"]) + "\n"
    lines += "Evaluation: " + str(trial["evaluation"]["objective"]) + "\n" if trial["evaluation"] else ""
    lines += "Score: " + str(trial["score"]["score"]) + "\n" if trial["score"] else ""
    return lines
