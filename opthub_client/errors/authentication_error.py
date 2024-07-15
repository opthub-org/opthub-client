"""This module contains the AuthenticationError class."""

import sys
from enum import Enum

import click


class AuthenticationErrorMessage(Enum):
    """Enum class for authentication error types."""

    LOGIN_FAILED = "Login failed. Please check your Username or Password."
    GET_JWKS_PUBLIC_KEY_FAILED = "Failed to get public key. Please try again later."


class AuthenticationError(Exception):
    """Exception raised for authentication related errors."""

    def __init__(self, error_type: AuthenticationErrorMessage) -> None:
        """Initialize the AuthenticationError class."""
        super().__init__(error_type.value)

    def handler(self) -> None:
        """Handle the GraphQL error."""
        click.echo(str(self))
        sys.exit(1)
