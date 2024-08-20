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

__all__ = ["raw", "OptHub", "Participant", "SubmitResult", "GetTrialResult"]


class Participant:
    """A class representing a match in a competition."""

    id: UUID

    def __init__(self, participant_id: UUID) -> None:
        """Creates a match instance from a match ID."""
        self.id = participant_id


class SubmitResult(NamedTuple):
    """A record representing the result of a solution submission."""

    match: str
    participant_type: raw.ParticipantType
    participant: str
    trial_no: int


class GetTrialResult(NamedTuple):
    """A record representing the result of trial retrieval."""

    match: str
    participant_type: raw.ParticipantType
    participant: str
    trial_no: int
    variable: NDArray[np.double]
    created_at: datetime
    user: str | None


class OptHub:
    """A class for accessing the OptHub public REST API."""

    client: raw.ApiClient
    endpoint = "https://example.com/todo/opthub-api-endpoint"

    def __init__(self, api_key: str) -> None:
        """Creates an instance for API access from an API key."""
        conf = raw.Configuration(host=self.endpoint)
        conf.api_key["ApiKeyAuth"] = api_key

        self.client = raw.ApiClient(conf)

    def submit(self, competition: str | None, match: str | None, solution: ArrayLike) -> SubmitResult:
        """Submit a solution."""
        vector = np.array(solution, dtype=np.double).flatten()
        match_id = self.resolve_match(competition, match)

        res = raw.SolutionApi(self.client).create_solution(match_id, vector)

        match = self.reverse_match(res.match_id)
        participant = self.reverse_participant(res.participant_id)
        return SubmitResult(match, res.participant_type, participant, res.trial_no)

    def get_trial(self, competition: str, match: str | None, participant: str | None, trial_no: int) -> GetTrialResult:
        """Retrieve a past submitted trial."""
        match_id = self.resolve_match(competition, match)
        participant_id = self.resolve_participant(participant)

        res = raw.SolutionApi(self.client).get_solution(match_id, participant_id, trial_no)

        match = self.reverse_match(res.match_id)
        participant = self.reverse_participant(res.participant_id)
        variable = np.array(res.variable, dtype=np.double)

        return GetTrialResult(match, res.participant_type, participant, trial_no, variable, res.created_at, res.user_id)

    def __enter__(self) -> Self:
        """A method to enable the use of the `with` statement."""
        self.client.__enter__()
        return self

    def __exit__(self, *args: object) -> None:
        """A method to enable the use of the `with` statement."""
        self.client.__exit__(*args)

    def resolve_match(self, competition: str, match: str) -> UUID | None:
        raise NotImplementedError

    def resolve_participant(self, participant: str) -> UUID | None:
        raise NotImplementedError

    def reverse_match(self, match_id: UUID) -> tuple[str, str]:
        raise NotImplementedError

    def reverse_participant(self, participant_id: UUID) -> str:
        raise NotImplementedError

    def reverse_user(self, user_id: UUID) -> str:
        raise NotImplementedError
