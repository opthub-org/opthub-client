"""This module contains the AuthenticationError class."""

import sys
from enum import Enum

import click


class AuthenticationErrorMessage(Enum):
    """Enum class for authentication error types."""

    LOGIN_FAILED = "Login failed. Please check your Username or Password."
    GET_JWKS_PUBLIC_KEY_FAILED = "Failed to get public key. Please try again later."
    LOAD_CREDENTIALS_FAILED = "Not found credentials. Please login with `opt login` command."
    REFRESH_FAILED = "Could not refresh access token. Please login again with `opt login` command."
    DECODE_JWT_TOKEN_FAILED = "Failed to decode JWT token. Please try again later."  # noqa: S105


class AuthenticationError(Exception):
    """Exception raised for authentication related errors."""

    def __init__(self, error_type: AuthenticationErrorMessage) -> None:
        """Initialize the AuthenticationError class."""
        super().__init__(error_type.value)

    def handler(self) -> None:
        """Handle the GraphQL error."""
        click.echo(str(self))
        sys.exit(1)
