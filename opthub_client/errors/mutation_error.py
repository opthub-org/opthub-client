"""This module contains the MutationError class."""

import sys
from enum import Enum

import click


class Method(Enum):
    """Enum class for mutation methods."""

    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class MutationError(Exception):
    """Exception raised for errors during mutations."""

    def __init__(self, method: Method, resource: str, detail: str) -> None:
        """Initialize the MutationError class."""
        self.method = method
        self.resource = resource
        self.detail = detail
        self.message = f"MutationError: {method} {resource} - {detail}"
        super().__init__(self.message)

    def handler(self) -> None:
        """Handle the mutation error."""
        click.echo(str(self))
        sys.exit(1)
