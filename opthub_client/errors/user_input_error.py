"""This module contains the UserInputError class."""


class UserInputError(Exception):
    """Exception raised for errors in user input."""

    def __init__(self, message: str) -> None:
        """Initialize the UserInputError class."""
        self.message = message
        super().__init__(self.message)
