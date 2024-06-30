"""This module contains the GraphQLError class."""


class GraphQLError(Exception):
    """Exception raised for errors in the GraphQL execution."""

    def __init__(self, message: str = "Unexpected error") -> None:
        """Initialize the GraphQLError class."""
        self.message = message
        super().__init__(self.message)
