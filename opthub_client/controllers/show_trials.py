"""This module contains the functions related to history command."""

import asyncio
import sys

import click
from prompt_toolkit import HTML, PromptSession
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from prompt_toolkit.styles import Style

from opthub_client.context.match_selection import MatchSelectionContext
from opthub_client.controllers.utils import check_current_version_status, get_trial_info_detail, get_trial_info_general
from opthub_client.models.trial import Trial, fetch_trials_async

style = Style.from_dict(
    {
        "n": "fg:blue bold",
        "e": "fg:red bold",
    },
)


def display_trials(trials: list[Trial], is_detail: bool) -> None:
    """Display the trials."""
    if trials is None:
        click.echo("No more solutions to display.")
    else:
        lines = ""
        for trial in trials:
            lines += get_trial_info_detail(trial) if is_detail else get_trial_info_general(trial)
        click.echo(lines.rstrip())


async def fetch_and_display_trials(selected_match_id: str, page: int, size: int, detail: bool) -> bool:
    """Fetch and display the trials. Returns True if trials were fetched, False if no more trials."""
    trials = await fetch_trials_async(selected_match_id, page, size)
    if not trials:
        return False
    run_in_terminal(lambda: display_trials(trials, detail), render_cli_done=False)
    return True


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
@click.pass_context
def show_trials(ctx: click.Context, competition: str | None, match: str | None, size: int, detail: bool) -> None:
    """Check submitted solutions."""
    # check_current_version_status()
    match_selection_context = MatchSelectionContext()
    selected_competition, selected_match = match_selection_context.get_selection(match, competition)
    bindings = KeyBindings()
    page = 0

    async def next_trials() -> None:
        nonlocal page
        page += 1
        if not await fetch_and_display_trials(selected_match["id"], page, size, detail):
            # No more trials, exit the application
            click.echo("All trials have been displayed.")
            sys.exit()

    # n key is to display next batch of solutions
    @bindings.add("n")
    def add_trials(event: KeyPressEvent) -> None:
        """Display next batch of solutions."""
        asyncio.create_task(next_trials())

    @bindings.add("e")  # e for exit
    @bindings.add("q")  # q for quit
    @bindings.add("c-c")  # Ctrl-C
    def exit_trials_view(event: KeyPressEvent) -> None:
        """Exit the application."""
        sys.exit()

    # Initialize prompt session with key bindings.
    session: PromptSession[str] = PromptSession(key_bindings=bindings)

    # The initial call to display next batch of solutions async.
    asyncio.run(fetch_and_display_trials(selected_match["id"], page, size, detail))

    # Prompt the user for more solutions(n key) or exit(e or q or Ctrl+c).
    session.prompt(
        HTML(
            '<n style="class:n">n</n>: next solutions, <e style="class:e">e</e>: exit \n',
        ),
        key_bindings=bindings,
        style=style,
    )
