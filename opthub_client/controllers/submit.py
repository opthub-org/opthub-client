"""This module contains the functions related to submit command."""

import json
from pathlib import Path

import click
from InquirerPy import prompt  # type: ignore[attr-defined]
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
def submit(match: str | None, competition: str | None, file: bool) -> None:
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
        # read the file
        if not isinstance(result, dict):
            # result is not a dictionary, cannot proceed
            return
        file_path = result.get("file")
        if not isinstance(file_path, str):
            # file_path is not a string, indicate error to user
            click.echo("The file path is incorrect. Please provide a valid file path.")
            return
        full_path = Path(file_path).expanduser()
        variable = json.loads(full_path.read_text())

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
        if not isinstance(result, dict) or "solution" not in result:
            # result is not a dict or "solution" is not in result
            click.echo("The input is missing. Please provide the necessary information.")
            return
        solution_value = result["solution"]
        if not isinstance(solution_value, str):
            # solution_value is not a string
            click.echo("The input format is incorrect. Please enter numbers separated by commas (e.g. 1.5,2.3,4.7)")
            return
        variable = json.loads(solution_value)
    click.echo(
        f"Submitting {variable} for Competition: {competition}, Match: {match}...",
    )
    create_solution(match, variable)
    click.echo("...Submitted.")
