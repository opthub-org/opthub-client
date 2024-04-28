"""This module contains the functions related to history command."""

import sys

import click
from prompt_toolkit import HTML, PromptSession
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from prompt_toolkit.styles import Style

from opthub_client import __version__
from opthub_client.context.match_selection import MatchSelectionContext
from opthub_client.graphql.version_cli import get_messages
from opthub_client.models.trial import Trial, fetch_trials

style = Style.from_dict(
    {
        "n": "fg:blue bold",
        "e": "fg:red bold",
    },
)


def display_trials(trials: list[Trial]) -> None:
    """Display the trials."""
    if trials is None:
        click.echo("No more solutions to display.")
    else:
        lines = ""
        for trial in trials:
            lines += "Trial No: " + str(trial["trialNo"]) + "\n"
            lines += "Solution: " + str(trial["solution"]["variable"]) + "\n"
            lines += "Evaluation: " + str(trial["evaluation"]["objective"]) + "\n"
            lines += "Score: " + str(trial["score"]["score"]) + "\n"
        click.echo(lines.rstrip())


@click.command()
@click.option(
    "-s",
    "--size",
    type=click.IntRange(1, 50),  # show size of trials must be 1-50
    default=10,
    help="Number of trials to display (1-50).",
)
@click.option("-c", "--competition", type=str, help="Competition ID.")
@click.option("-m", "--match", type=str, help="Match ID.")
@click.pass_context
def history(ctx: click.Context, competition: str | None, match: str | None, size: int) -> None:
    """Check submitted solutions."""
    message = get_messages(__version__)
    if message.label == "Error":
        click.echo(click.style(message.message, fg="red"))
        return
    match_selection_context = MatchSelectionContext()
    selected_competition, selected_match = match_selection_context.get_selection(match, competition)
    bindings = KeyBindings()

    # n key is to display next batch of solutions
    @bindings.add("n")
    def add_trials(event: KeyPressEvent) -> None:
        """Display next batch of solutions."""
        trials = fetch_trials(selected_competition["id"], selected_match["id"], 1, size)
        run_in_terminal(lambda: display_trials(trials), render_cli_done=False)

    @bindings.add("e")  # e for exit
    @bindings.add("q")  # q for quit
    @bindings.add("c-c")  # Ctrl-C
    def exit_trials_view(event: KeyPressEvent) -> None:
        """Exit the application."""
        sys.exit()

    # Initialize prompt session with key bindings.
    session: PromptSession[str] = PromptSession(key_bindings=bindings)

    # The initial call to display next batch of solutions.
    # (Directly using the logic inside the _ function above.)
    trials = fetch_trials(selected_competition["id"], selected_match["id"], 1, size)
    display_trials(trials)
    while True:
        # Prompt the user for more solutions(n key) or exit(e or q or Ctrl+c).
        session.prompt(
            HTML(
                '<n style="class:n">n</n>: more solutions, <e style="class:e">e</e>: exit \n',
            ),
            key_bindings=bindings,
            style=style,
        )
