"""This module contains the functions related to history command."""

import asyncio

import click
from prompt_toolkit import HTML, PromptSession
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent

from opthub_client.context.match_selection import MatchSelectionContext
from opthub_client.controllers.utils import check_current_version_status
from opthub_client.models.trial import fetch_trials_async
from opthub_client.view.display_trials import display_trials, user_interaction_message, user_interaction_message_style


async def fetch_and_display_trials(selected_match_id: str, page: int, size: int, detail: bool, desc: bool) -> bool:
    """Fetch and display the trials. Returns True if more trials are available, False if no more trials.

    Args:
        selected_match_id (str): selected match id
        page (int): Page number
        size (int): Number of trials to display
        detail (bool): True for detailed information, false for general information
        desc (bool): True for show trials in descending order, false for ascending order

    Returns:
        bool: True if more trials are available, False if no more trials
    """
    trials, is_first, is_last = await fetch_trials_async(selected_match_id, page, size, desc)
    run_in_terminal(lambda: display_trials(trials, detail), render_cli_done=False)
    return (desc and is_first) or (not desc and is_last)


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
@click.option("-desc", "--descending", is_flag=True, help="Show trials in descending order")
@click.pass_context
def show_trials(
    ctx: click.Context, competition: str | None, match: str | None, size: int, detail: bool, descending: bool
) -> None:
    """Check submitted solutions."""
    # check_current_version_status()
    match_selection_context = MatchSelectionContext()
    selected_match = match_selection_context.get_selection_match(match, competition)
    bindings = KeyBindings()
    page = 0
    has_all_trials_displayed = False
    tasks = []

    async def next_trials() -> None:
        nonlocal page, has_all_trials_displayed
        page += 1
        has_more_trials = await fetch_and_display_trials(selected_match["id"], page, size, detail, descending)
        if has_more_trials:
            # No more trials, display the message and set the flag.
            has_all_trials_displayed = True
            run_in_terminal(lambda: click.echo("All trials have been displayed."), render_cli_done=False)

    # n key is to display next batch of solutions
    @bindings.add("n")
    def add_trials(event: KeyPressEvent) -> None:
        """Display next batch of solutions."""
        if not has_all_trials_displayed:
            task = asyncio.create_task(next_trials())
            tasks.append(task)
        else:
            run_in_terminal(lambda: click.echo("All trials have been displayed."), render_cli_done=False)

    @bindings.add("e")  # e for exit
    @bindings.add("q")  # q for exit
    @bindings.add("c-c")  # Ctrl-C for exit
    def exit_trials_view(event: KeyPressEvent) -> None:
        """Exit the application."""
        session.app.exit()

    # Initialize prompt session with key bindings.
    session: PromptSession[str] = PromptSession(key_bindings=bindings)

    # The initial call to display next batch of solutions async.
    asyncio.run(fetch_and_display_trials(selected_match["id"], page, size, detail, descending))
    # Prompt the user for more solutions(n key) or exit(e or q or Ctrl+c).
    session.prompt(
        HTML(user_interaction_message()),
        key_bindings=bindings,
        style=user_interaction_message_style(),
    )
