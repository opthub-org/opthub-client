"""This module contains the GraphQLError class."""

import sys

import click


class GraphQLError(Exception):
    """Exception raised for errors in the GraphQL execution."""

    def __init__(self, message: str) -> None:
        """Initialize the GraphQLError class."""
        self.message = message
        super().__init__(self.message)

    def handler(self) -> None:
        """Handle the GraphQL error."""
        click.echo(str(self))
        sys.exit(1)
