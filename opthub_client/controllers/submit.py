"""This module contains the functions related to submit command."""

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
        if isinstance(result, dict):
            file_path = result.get("file")
            if isinstance(file_path, str):
                full_path = Path(file_path).expanduser()
                variable = [float(x) for x in full_path.read_text().split(",")]
            else:
                # file_path is not a string
                click.echo("The file path is incorrect. Please provide a valid file path.")
                return
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
        if isinstance(result, dict) and "solution" in result:
            solution_value = result["solution"]
            if isinstance(solution_value, str):
                variable = [float(x) for x in solution_value.split(",")]
            else:
                # solution_value is not a string
                click.echo("The input format is incorrect. Please enter numbers separated by commas (e.g. 1.5,2.3,4.7)")
                return
        else:
            # result is not a dict or "solution" is not in result
            click.echo("The input is missing. Please provide the necessary information.")
            return
    click.echo(
        f"Submitting {variable} for Competition: {competition}, Match: {match}...",
    )
    create_solution(match, variable)
    click.echo("...Submitted.")
