"""This module contains the CacheIOError class."""

import sys
from enum import Enum

import click


class CacheIOErrorMessage(Enum):
    """Enum class for cacheIO error types."""

    VERSION_FILE_READ_FAILED = "Failed to read version cache file. Please try again later."
    MATCH_SELECTION_FILE_READ_FAILED = "Failed to read match selection cache file. Please try again later."
    WRITE_FAILED = "Failed to write cache file. Please try again later."
    MATCH_NOT_SELECTED = "Please select a match first."


class CacheIOError(Exception):
    """Exception raised for errors in cache file I/O."""

    def __init__(self, error_type: CacheIOErrorMessage) -> None:
        """Initialize the CacheIOError class."""
        super().__init__(error_type.value)

    def handler(self) -> None:
        """Handle the cache file I/O error."""
        click.echo(str(self))
        sys.exit(1)
