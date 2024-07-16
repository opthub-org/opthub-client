"""This module contains the functions related to submit command."""

from pathlib import Path

import click
from InquirerPy import prompt  # type: ignore[attr-defined]
from InquirerPy.validator import PathValidator

from opthub_client.context.match_selection import MatchSelectionContext
from opthub_client.controllers.utils import check_current_version_status
from opthub_client.errors.authentication_error import AuthenticationError
from opthub_client.errors.cache_io_error import CacheIOError
from opthub_client.errors.mutation_error import MutationError
from opthub_client.errors.user_input_error import UserInputError, UserInputErrorMessage
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
def submit(ctx: click.Context, match: str | None, competition: str | None, file: bool) -> None:  # noqa: ARG001
    """Submit a solution."""
    try:
        check_current_version_status()
        match_selection_context = MatchSelectionContext()
        selected_competition, selected_match = match_selection_context.get_selection(match, competition)
        raw_solution_value = get_file_submission() if file else get_text_submission()
        if not SolutionValidator.check_solution(raw_solution_value):
            raise UserInputError(UserInputErrorMessage.SOLUTION_ERROR)
        click.echo(
            f"Submitting to {selected_competition['alias']}/{selected_match['alias']}...",
        )
        create_solution(selected_match["id"], raw_solution_value)
        click.echo("...Submitted.")
    except (AuthenticationError, MutationError, CacheIOError, UserInputError) as error:
        error.handler()
    except Exception:
        click.echo("Unexpected error occurred. Please try again later.")


def get_file_submission() -> str:
    """Get solution from the file submission.

    Raises:
        UserInputError: If the solution is not provided.

    Returns:
        str: solution text
    """
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
    if not isinstance(result, dict):
        raise UserInputError(UserInputErrorMessage.FILE_ERROR)
    file_path = result.get("file")
    if not isinstance(file_path, str):
        raise UserInputError(UserInputErrorMessage.FILE_PATH_ERROR)
    full_path = Path(file_path).expanduser()
    return full_path.read_text()


def get_text_submission() -> str:
    """Get solution from the text submission.

    Raises:
        UserInputError: If the solution is not provided.

    Returns:
        str: solution text
    """
    questions = [
        {
            "name": "solution",
            "type": "input",
            "message": "Write the solution:",
        },
    ]
    result = prompt(questions)
    if not isinstance(result, dict) or "solution" not in result:
        raise UserInputError(UserInputErrorMessage.SOLUTION_ERROR)
    return str(result["solution"])
