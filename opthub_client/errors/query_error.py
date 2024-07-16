"""This module contains the QueryError class."""

import sys

import click


class QueryError(Exception):
    """Exception raised for errors during query data processing."""

    def __init__(self, resource: str, detail: str) -> None:
        """Initialize the QueryError class."""
        self.resource = resource
        self.detail = detail
        self.message = f"QueryError: {resource} - {detail}"
        super().__init__(self.message)

    def handler(self) -> None:
        """Handle the query error."""
        click.echo(str(self))
        sys.exit(1)
