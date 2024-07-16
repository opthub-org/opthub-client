"""This module contains the functions related to history command."""

import asyncio

import click
from prompt_toolkit import HTML, PromptSession
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent

from opthub_client.context.match_selection import MatchSelectionContext
from opthub_client.controllers.utils import check_current_version_status
from opthub_client.errors.authentication_error import AuthenticationError
from opthub_client.errors.cache_io_error import CacheIOError
from opthub_client.errors.fetch_error import FetchError
from opthub_client.errors.query_error import QueryError
from opthub_client.errors.user_input_error import UserInputError
from opthub_client.models.trial import fetch_trials_async
from opthub_client.view.display_trials import display_trials, user_interaction_message, user_interaction_message_style


@click.command(name="trials")
@click.option("-c", "--competition", type=str, help="Competition ID.")
@click.option("-m", "--match", type=str, help="Match ID.")
@click.option("-d", "--detail", is_flag=True, help="Show detailed information")
@click.option(
    "-s",
    "--size",
    type=click.IntRange(1, 50),  # show size of trials must be 1-50
    default=20,
    help="Number of trials to display (1-50).",
)
@click.option(
    "-f",
    "--from",
    "trial_from",
    type=int,
    default=0,
    help="Number of trials to display (1-50).",
)
@click.option("-asc", "--ascending", is_flag=True, help="Show trials in ascending order")
@click.option("-suc", "--success", is_flag=True, help="Show only successful trials")
@click.pass_context
def show_trials(
    ctx: click.Context,  # noqa: ARG001
    competition: str | None,
    match: str | None,
    size: int,
    trial_from: int,
    detail: bool,
    ascending: bool,
    success: bool,
) -> None:
    """Check submitted solutions."""
    try:
        check_current_version_status()
        match_selection_context = MatchSelectionContext()
        selected_match = match_selection_context.get_match(match, competition)
        bindings = KeyBindings()
        page = 0
        has_all_trials_displayed = False
        tasks = []
        # trial_from is 0 and ascending is True, then increment trial_from by 1 because trial number starts from 1.
        trial_from = trial_from + 1 if trial_from == 0 and ascending else trial_from

        async def next_trials() -> None:
            nonlocal page, has_all_trials_displayed
            page += 1
            has_more_trials = await fetch_and_display_trials(
                selected_match["id"],
                page,
                size,
                trial_from,
                detail,
                ascending,
                success,
            )
            if not has_more_trials:
                # No more trials, display the message and set the flag.
                has_all_trials_displayed = True

        # n key is to display next batch of solutions
        @bindings.add("n")
        def add_trials(event: KeyPressEvent) -> None:  # noqa: ARG001
            """Display next batch of solutions."""
            if not has_all_trials_displayed:
                task = asyncio.create_task(next_trials())
                tasks.append(task)
            else:
                run_in_terminal(lambda: click.echo("No more trials."), render_cli_done=False)

        @bindings.add("e")  # e for exit
        @bindings.add("q")  # q for exit
        @bindings.add("c-c")  # Ctrl-C for exit
        def exit_trials_view(event: KeyPressEvent) -> None:  # noqa: ARG001
            """Exit the application."""
            session.app.exit()

        # Initialize prompt session with key bindings.
        session: PromptSession[str] = PromptSession(key_bindings=bindings)

        # The initial call to display next batch of solutions async.
        has_more_trials = asyncio.run(
            fetch_and_display_trials(
                selected_match["id"],
                page,
                size,
                trial_from,
                detail,
                ascending,
                success,
            ),
        )
        if not has_more_trials:
            has_all_trials_displayed = True
        # Prompt the user for more solutions(n key) or exit(e or q or Ctrl+c).
        session.prompt(
            HTML(user_interaction_message()),
            key_bindings=bindings,
            style=user_interaction_message_style(),
        )
    except (AuthenticationError, FetchError, QueryError, CacheIOError, UserInputError) as error:
        error.handler()


async def fetch_and_display_trials(
    selected_match_id: str,
    page: int,
    size: int,
    trial_from: int,
    detail: bool,
    asc: bool,
    success: bool,
) -> bool:
    """Fetch and display the trials. Returns True if more trials are available, False if no more trials.

    Args:
        selected_match_id (str): selected match id
        page (int): Page number
        size (int): Number of trials to display
        trial_from (int): Trial number to start from
        detail (bool): True for detailed information, false for general information
        asc (bool): True for show trials in ascending order, false for descending order
        success (bool): True for show only successful trials, false for all trials

    Returns:
        bool: True if more trials are available, False if no more trials
    """
    trials, is_first, is_last = await fetch_trials_async(
        match_id=selected_match_id,
        page=page,
        page_size=size,
        limit=size,
        offset=trial_from,
        is_asc=asc,
        display_only_success=success,
    )
    run_in_terminal(lambda: display_trials(trials, detail), render_cli_done=False)
    if (asc and is_last) or (not asc and is_first):
        run_in_terminal(lambda: click.echo("No more trials."), render_cli_done=False)
        return False
    return True
