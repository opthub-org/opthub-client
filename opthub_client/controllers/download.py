"""Download trials to a file."""

import json
from pathlib import Path

import click

from opthub_client.context.match_selection import MatchSelectionContext
from opthub_client.controllers.utils import check_current_version_status
from opthub_client.models.trial import fetch_trials


@click.command()
@click.option("-c", "--competition", type=str, help="Competition ID.")
@click.option("-m", "--match", type=str, help="Match ID.")
@click.option(
    "-l",
    "--limit",
    type=click.IntRange(1, 50),  # show size of trials must be 1-50
    default=20,
    help="Number of trials to download (1-50).",
)
@click.option(
    "-s",
    "--start",
    type=click.INT,
    default=1,
    help="Starting trial number",
)
@click.pass_context
def download(ctx: click.Context, competition: str | None, match: str | None, limit: int, start: int) -> None:
    """Download trials to a file."""
    check_current_version_status()
    match_selection_context = MatchSelectionContext()
    selected_match = match_selection_context.get_match(match, competition)

    trials = fetch_trials(selected_match["id"], trial_no=start, size=limit)
    output_file = Path(f"trials_{selected_match['alias']}_trial{start}-{start+limit-1}.json")

    # Write trials to a JSON file
    with output_file.open("w") as f:
        json.dump(trials, f, indent=4)

    click.echo(f"Trials have been written to {output_file}")
