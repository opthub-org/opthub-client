"""This module contains the FetchError class."""

import sys

import click


class FetchError(Exception):
    """Exception raised for errors in the Fetch execution."""

    def __init__(self, message: str) -> None:
        """Initialize the FetchError class."""
        self.message = message
        super().__init__(self.message)

    def handler(self) -> None:
        """Handle the Fetch error."""
        click.echo(str(self))
        sys.exit(1)
