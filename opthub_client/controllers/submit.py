"""This module contains the functions related to submit command."""

import json
from pathlib import Path

import click
from InquirerPy import prompt
from InquirerPy.validator import PathValidator

from opthub_client.context.match_selection import MatchSelectionContext
from opthub_client.models.solution import create_solution
from opthub_client.validators.solution import SolutionValidator


@click.command()
@click.option(
    "-c",
    "--competition",
    type=str,
    help="Competition ID",
)
@click.option(
    "-m",
    "--match",
    type=str,
    help="Match ID",
)
@click.option(
    "-f",
    "--file",
    is_flag=True,
    help="Flag to indicate file submission.",
)
@click.pass_context
def submit(ctx: click.Context, match: str, competition: str, file: bool) -> None:
    """Submit a solution."""
    match_selection_context = MatchSelectionContext()
    if match is None:
        match = match_selection_context.match_id
    if competition is None:
        competition = match_selection_context.competition_id
    if competition is None or match is None:
        click.echo("Please select a competition and match first.")
        return
    if file:  # file submission
        questions = [
            {
                "name": "file",
                "type": "filepath",
                "message": "Submit the solution file (must be a JSON file):",
                "default": str(Path("~/")),
                "validate": PathValidator(is_file=True, message="Input is not a file"),
                "only_files": True,
            },
        ]
        result = prompt(questions)
        variable = Path(result).read_text()
    else:  # text submission
        questions = [
            {
                "name": "solution",
                "type": "input",
                "message": "Write the solution:",
                "validate": SolutionValidator(),
            },
        ]
        result = prompt(questions)
        variable = [float(x) for x in result["solution"].split(",")]
        variable = json.dumps(variable)
    click.echo(
        f"Submitting {result} for Competition: {competition}, Match: {match}...",
    )
    create_solution(match, variable)
    click.echo("...Submitted.")
