"""This module contains the functions related to history command."""

import click

from opthub_client.context.match_selection import MatchSelectionContext
from opthub_client.controllers.utils import check_current_version_status
from opthub_client.errors.authentication_error import AuthenticationError
from opthub_client.errors.cache_io_error import CacheIOError
from opthub_client.errors.fetch_error import FetchError
from opthub_client.errors.query_error import QueryError
from opthub_client.errors.user_input_error import UserInputError
from opthub_client.models.trial import fetch_trial
from opthub_client.view.display_trials import display_trial


@click.command(name="trial")
@click.option("-c", "--competition", type=str, help="Competition ID.")
@click.option("-m", "--match", type=str, help="Match ID.")
@click.option("-d", "--detail", is_flag=True, help="Show detailed information")
@click.argument("trial_no", type=int, required=True)
@click.pass_context
def show_trial(
    ctx: click.Context,  # noqa: ARG001
    competition: str | None,
    match: str | None,
    detail: bool,
    trial_no: int,
) -> None:
    """Check submitted solution."""
    try:
        check_current_version_status()
        match_selection_context = MatchSelectionContext()
        selected_match = match_selection_context.get_match(match, competition)
        # display batch of solutions.
        trial = fetch_trial(selected_match["id"], trial_no=trial_no)
        display_trial(trial, detail)
    except (AuthenticationError, FetchError, QueryError, CacheIOError, UserInputError) as error:
        error.handler()
    except Exception:
        click.echo("Unexpected error occurred. Please try again later.")
