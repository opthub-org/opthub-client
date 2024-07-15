"""This module contains the UserInputError class."""

import sys
from enum import Enum

import click


class UserInputErrorMessage(Enum):
    """Enum class for user input error types."""

    INPUT_FILE_ERROR = "File input error. Please check the file."
    INPUT_FILE_PATH_ERROR = "File path error. Please check the file path."
    INPUT_SOLUTION_ERROR = "Solution input error. Please check the solution."
    INPUT_MATCH_ERROR = "Match input error. Please check the match."
    INPUT_COMPETITION_ERROR = "Competition input error. Please check the competition."


class UserInputError(Exception):
    """Exception raised for errors in user input."""

    def __init__(self, error_type: UserInputErrorMessage) -> None:
        """Initialize the UserInputError class."""
        super().__init__(error_type.value)

    def handler(self) -> None:
        """Handle the user input error."""
        click.echo(str(self))
        sys.exit(1)
