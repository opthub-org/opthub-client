"""Access to the OptHub public REST API.

The module is designed to wrap a library that is automatically generated from the OpenAPI schema
to access the OptHub public REST API.

The automatically generated raw Python package is available at https://github.com/opthub-org/opthub-api-client-python.
"""

from datetime import datetime
from typing import NamedTuple, Self
from uuid import UUID

import numpy as np
import opthub_api_client as raw
from numpy.typing import ArrayLike, NDArray
from opthub_api_client import ParticipantType

__all__ = ["raw", "OptHub", "Match", "Participant", "Competition", "SubmitResult", "GetTrialResult", "ParticipantType"]


class Participant(NamedTuple):
    """A class representing a participant."""

    id: UUID
    type: ParticipantType

    @property
    def alias(self) -> str:
        """Retrieve the alias name of the participant."""
        raise NotImplementedError


class SubmitResult(NamedTuple):
    """A record representing the result of a solution submission."""

    participant: Participant
    trial_no: int


class GetTrialResult(NamedTuple):
    """A record representing the result of trial retrieval."""

    participant: Participant
    variable: NDArray[np.double]
    created_at: datetime
    user: str | None


class Match:
    """A class representing a match in a competition."""

    id: UUID
    client: raw.ApiClient

    def submit(self, solution: ArrayLike) -> SubmitResult:
        """Submit a solution."""
        vector = np.array(solution, dtype=np.double).flatten()

        res = raw.SolutionApi(self.client).create_solution(self.id, vector)

        return SubmitResult(Participant(res.participant_id, res.participant_type), res.trial_no)

    def get_trial(self, participant: Participant, trial_no: int) -> GetTrialResult | None:
        """Retrieve a past submitted trial."""
        res = raw.SolutionApi(self.client).get_solution(self.match, participant.id, trial_no)

        variable = np.array(res.variable, dtype=np.double)

        return GetTrialResult(
            Participant(res.participant_id, res.participant_type),
            variable,
            res.created_at,
            res.user_id,
        )

    @property
    def alias(self) -> str:
        """Retrieve the alias name of the match."""
        raise NotImplementedError


class Competition:
    """A class representing a competition."""

    id: UUID
    client: raw.ApiClient

    @property
    def alias(self) -> str:
        """Retrieve the alias name of the competition."""
        raise NotImplementedError

    def match(self, alias: str | None) -> Match:
        """Retrieve a match by its alias name.

        If no alias name is specified, return the default one.
        """
        raise NotImplementedError


class OptHub:
    """A class for accessing the OptHub public REST API."""

    client: raw.ApiClient
    endpoint = "https://example.com/todo/opthub-api-endpoint"

    def __init__(self, api_key: str) -> None:
        """Creates an instance for API access from an API key."""
        conf = raw.Configuration(host=self.endpoint)
        conf.api_key["ApiKeyAuth"] = api_key

        self.client = raw.ApiClient(conf)

    def competition(self, alias: str | None) -> Competition:
        """Retrieve a competition by its alias name.

        If no alias name is specified, return the default one.
        """
        raise NotImplementedError

    def __enter__(self) -> Self:
        """A method to enable the use of the `with` statement."""
        self.client.__enter__()
        return self

    def __exit__(self, *args: object) -> None:
        """A method to enable the use of the `with` statement."""
        self.client.__exit__(*args)
