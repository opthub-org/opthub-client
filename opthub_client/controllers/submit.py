"""This module contains the functions related to submit command."""

from pathlib import Path

import click
from InquirerPy import prompt  # type: ignore[attr-defined]
from InquirerPy.validator import PathValidator

from opthub_client.context.match_selection import MatchSelectionContext
from opthub_client.controllers.utils import check_current_version_status
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
    """Submit a solution.

    Args:
        match (str | None): option for match(-m or --match)
        competition (str | None): option for competition(-c or --competition)
        file (bool): option for file(-f or --file). if -f or --file is provided, it will be a file submission.
    """
    check_current_version_status()
    match_selection_context = MatchSelectionContext()
    selected_competition, selected_match = match_selection_context.get_selection(match, competition)
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
        raw_solution_value = full_path.read_text()
    else:  # text submission
        questions = [
            {
                "name": "solution",
                "type": "input",
                "message": "Write the solution:",
            },
        ]
        result = prompt(questions)
        if not isinstance(result, dict) or "solution" not in result:
            # result is not a dict or "solution" is not in result
            click.echo("The input is missing. Please provide the necessary information.")
            return
        raw_solution_value = str(result["solution"])
    if not SolutionValidator.check_solution(raw_solution_value):
        click.echo("The solution is not valid. Please provide a valid solution.")
        return
    click.echo(
        f"Submitting to {selected_competition['alias']}/{selected_match['alias']}...",
    )
    create_solution(selected_match["id"], raw_solution_value)
    click.echo("...Submitted.")
