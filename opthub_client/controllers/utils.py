"""Util for opthub_client."""

import sys

import click

from opthub_client.context.read_version import get_version_from_file
from opthub_client.graphql.version_cli import get_version_status_messages
from opthub_client.models.trial import Trial


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
