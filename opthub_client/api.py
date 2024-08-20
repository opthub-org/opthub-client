"""Access to the OptHub public REST API.

The module is designed to wrap a library that is automatically generated from the OpenAPI schema
to access the OptHub public REST API.

The automatically generated raw Python package is available at https://github.com/opthub-org/opthub-api-client-python.
"""

from typing import Self
from uuid import UUID

import numpy as np
import opthub_api_client as raw
from numpy.typing import ArrayLike

__all__ = ["raw", "OptHub", "Match"]


class Match:
    """A class representing a match in a competition."""

    id: UUID

    def __init__(self, match_id: UUID) -> None:
        """Creates a match instance from a match ID."""
        self.id = match_id


class OptHub:
    """A class for accessing the OptHub public REST API."""

    client: raw.ApiClient

    def __init__(self, api_key: str) -> None:
        """Creates an instance for API access from an API key."""
        conf = raw.Configuration(host=endpoint)
        conf.api_key["ApiKeyAuth"] = api_key

        self.client = raw.ApiClient(conf)

    def submit(self, match: Match, solution: ArrayLike) -> None:
        """Submit a solution."""
        vector = list(np.array(solution, dtype=np.double).flatten())
        raw.SolutionApi(self.client).create_solution(match.id, vector)

    def __enter__(self) -> Self:
        """A method to enable the use of the `with` statement."""
        self.client.__enter__()
        return self

    def __exit__(self, *args: object) -> None:
        """A method to enable the use of the `with` statement."""
        self.client.__exit__(*args)


endpoint = "https://example.com/todo/opthub-api-endpoint"
