"""This module contains the MutationError class."""


class MutationError(Exception):
    """Exception raised for errors during mutations."""

    def __init__(self, method: str, resource: str, detail: str) -> None:
        """Initialize the MutationError class."""
        self.method = method
        self.resource = resource
        self.detail = detail
        self.message = f"MutationError: {method} {resource} - {detail}"
        super().__init__(self.message)
