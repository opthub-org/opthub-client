"""This module contains the functions related to submit command."""

import json
from pathlib import Path
from typing import cast

import click
from InquirerPy import prompt  # type: ignore[attr-defined]
from InquirerPy.validator import PathValidator

from opthub_client.context.match_selection import MatchSelectionContext
from opthub_client.controllers.utils import version_message
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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    version_message()
=======
    message = get_messages(__version__)
=======
    message = get_messages(get_version())
>>>>>>> 6d216d1 (:sparkles: add read version from toml file1)
    if message.label == "Error":
        click.echo(click.style(message.label, fg=message.labelColor))
        click.echo(click.style(message.message, fg=message.messageColor))
        return
>>>>>>> 8a5b4f8 (:sparkles: add library message)
=======
    version_message()
>>>>>>> e56224c (:art: use compornent)
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
        variable = json.loads(full_path.read_text())

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
        solution_value = result["solution"]
        if not isinstance(solution_value, str):
            # solution_value is not a string
            click.echo("The input format is incorrect. Please enter numbers separated by commas (e.g. [1.5,2.3,4.7])")
            return
        variable = json.loads(solution_value)
    if not SolutionValidator.check_solution(variable):
        click.echo("The solution is not valid. Please provide a valid solution.")
        return
    variable = cast(list[float], variable)
    click.echo(
        f"Submitting {variable} for Competition: {selected_competition['alias']}, Match: {selected_match['alias']}...",
    )
    create_solution(selected_match["id"], variable)
    click.echo("...Submitted.")
