"""Download trials to a file."""

import json
from pathlib import Path

import click

from opthub_client.context.match_selection import MatchSelectionContext
from opthub_client.controllers.utils import check_current_version_status
from opthub_client.models.trial import fetch_trials

SIZE_FETCH_TRIALS = 50


@click.command()
@click.option("-c", "--competition", type=str, help="Competition ID.")
@click.option("-m", "--match", type=str, help="Match ID.")
@click.option(
    "-s",
    "--start",
    type=click.IntRange(min=1),
    default=1,
    help="Start trial number",
)
@click.option(
    "-e",
    "--end",
    type=click.IntRange(min=1),
    default=SIZE_FETCH_TRIALS,
    help="End trial number",
)
@click.option("-desc", "--descending", is_flag=True, help="Show trials in descending order")
@click.option("-suc", "--success", is_flag=True, help="Show only successful trials")
@click.pass_context
def download(
    ctx: click.Context,
    competition: str | None,
    match: str | None,
    start: int,
    end: int,
    descending: bool,
    success: bool,
) -> None:
    """Download trials to a file."""
    check_current_version_status()
    match_selection_context = MatchSelectionContext()
    selected_match = match_selection_context.get_match(match, competition)
    output_file = Path(f"trials_{selected_match['alias']}_trials.json")
    total_trials = end - start + 1

    with open(output_file, "w") as f:
        all_trials = []
        with click.progressbar(
            length=total_trials,
            label="Downloading trials",
        ) as bar:
            for batch_start in range(start, end + 1, SIZE_FETCH_TRIALS):
                limit = min(SIZE_FETCH_TRIALS, end - batch_start + 1)
                trials, is_first, is_last = fetch_trials(
                    selected_match["id"],
                    start=batch_start,
                    limit=limit,
                    is_desc=descending,
                    display_only_success=success,
                )
                all_trials.extend(trials)
                if (is_first and descending) or (is_last and not descending):
                    bar.update(total_trials)
                    break
                bar.update(limit)
        json.dump(all_trials, f, indent=4)

    click.echo(f"Trials have been written to {output_file}")
