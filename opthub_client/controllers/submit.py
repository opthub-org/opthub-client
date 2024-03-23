"""This module contains the functions related to submit command."""

import json
from pathlib import Path

import click
from InquirerPy import prompt  # type: ignore[attr-defined]
from InquirerPy.validator import PathValidator

from opthub_client.context.match_selection import match_select
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
def submit(match: str | None, competition: str | None, file: bool) -> None:
    """Submit a solution."""
    selected_competition,selected_match = match_select(match, competition)
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
        f"Submitting {result} for Competition: {selected_competition['alias']}, Match: {selected_match['alias']}...",
    )
    create_solution(selected_match["id"], variable)
    click.echo("...Submitted.")
