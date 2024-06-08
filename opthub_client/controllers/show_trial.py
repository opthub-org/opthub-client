"""This module contains the functions related to history command."""

import click

from opthub_client.context.match_selection import MatchSelectionContext
from opthub_client.controllers.utils import check_current_version_status, get_trial_info_detail, get_trial_info_general
from opthub_client.models.trial import Trial, fetch_trial


def display_trial(trial: Trial, is_detail: bool) -> None:
    """Display the trials."""
    if trial is None:
        click.echo("No more solutions to display.")
    else:
        lines = get_trial_info_detail(trial) if is_detail else get_trial_info_general(trial)
        click.echo(lines.rstrip())


@click.command(name="trial")
@click.option("-c", "--competition", type=str, help="Competition ID.")
@click.option("-m", "--match", type=str, help="Match ID.")
@click.option("-d", "--detail", is_flag=True, help="Show detailed information")
@click.argument("trial_no", type=int, required=True)
@click.pass_context
def show_trial(ctx: click.Context, competition: str | None, match: str | None, detail: bool, trial_no: int) -> None:
    """Check submitted solutions."""
    # check_current_version_status()
    match_selection_context = MatchSelectionContext()
    selected_competition, selected_match = match_selection_context.get_selection(match, competition)

    # The initial call to display next batch of solutions.
    # (Directly using the logic inside the _ function above.)
    trial = fetch_trial(selected_match["id"], trial_no=trial_no)
    display_trial(trial, detail)
