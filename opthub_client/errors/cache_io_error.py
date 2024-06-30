"""This module contains the CacheIOError class."""

from enum import Enum


class CacheIOErrorMessage(Enum):
    """Enum class for cacheIO error types."""

    VERSION_FILE_READ_FAILED = "Failed to read version cache file. Please try again later."
    WRITE_FAILED = "Failed to write cache file. Please try again later."


class CacheIOError(Exception):
    """Exception raised for errors in cache file I/O."""

    def __init__(self, error_type: CacheIOErrorMessage) -> None:
        """Initialize the CacheIOError class."""
        super().__init__(error_type.value)
