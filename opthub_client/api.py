"""Access to the OptHub public REST API.

The module is designed to wrap a library that is automatically generated from the OpenAPI schema
to access the OptHub public REST API.

The automatically generated raw Python package is available at https://github.com/opthub-org/opthub-api-client-python.
"""

from collections.abc import Callable
from time import sleep
from typing import NamedTuple, Self
from uuid import UUID

import numpy as np
import opthub_api_client as raw
from numpy.typing import ArrayLike
from opthub_api_client import MatchTrialEvaluation, MatchTrialScore

__all__ = ["raw", "OptHub", "Match", "TrialStatus", "SubmitResult", "MatchTrialEvaluation", "MatchTrialScore"]


class TrialStatus(NamedTuple):
    """A record representing the result of trial status retrieval."""

    type: raw.MatchTrialStatusType
    evaluation: raw.MatchTrialEvaluation | None
    score: raw.MatchTrialScore | None


class SubmitResult:
    """A class representing the result of a solution submission."""

    trial_no: int
    match: "Match"

    def wait_evaluation(self) -> TrialStatus:
        """Wait until the evaluation is complete, then return the results."""
        self._poll(lambda: self.get_trial(), lambda trial: trial.evaluation.type != MatchTrialEvaluation.EVALUATING)

    def wait_scoring(self) -> TrialStatus:
        """Wait until the scoring is complete, then return the results."""
        self._poll(
            lambda: self.get_trial(),
            lambda trial: trial.evaluation.type not in {MatchTrialEvaluation.EVALUATING, MatchTrialEvaluation.SCORING},
        )

    def get_trial(self) -> TrialStatus:
        """Retrieves the status of the trial.

        Wait until the submitted results are reflected on the server side and the trial information becomes available.
        """
        self._poll(self.try_get_trial(self.trial_no), lambda trial: trial is not None)

    def _poll[T](self, callback: Callable[[], T], finish: Callable[[T], bool]) -> T:
        while True:
            result = callback()
            if finish(result):
                return result
            sleep(self.match.api.poll_interval_sec)

    def __del__(self) -> None:
        """Release the parent reference for GC."""
        self.match = None


class Match:
    """A class representing a match in a competition."""

    uuid: UUID
    api: "OptHub"

    def submit(self, solution: ArrayLike) -> SubmitResult:
        """Submit a solution."""
        vector = np.array(solution, dtype=np.double).flatten()

        response = raw.SolutionApi(self.api.client).create_solution(str(self.uuid), vector)

        result = SubmitResult()
        result.trial_no = response.trial_no
        result.api = self.api
        return result

    def try_get_trial(self, trial_no: int) -> TrialStatus | None:
        """Retrieves the status of the trial with the specified trial number.

        If the corresponding trial number does not exist, it returns `None`.
        """
        try:
            response = raw.TrialApi(self.api.client).get_match_trial(str(self.uuid), trial_no)
            return TrialStatus(response.type, response.evaluation, response.score)

        except raw.exceptions.NotFoundException as e:
            if e.body == '"NoSuchTrialNo"':
                return None
            raise

    def get_trial(self, trial_no: int) -> TrialStatus:
        """Retrieves the status of the trial with the specified trial number.

        If the corresponding trial number does not exist, an exception is raised.
        """
        trial = self.try_get_trial(trial_no)

        if trial is None:
            msg = "No such trial number."
            raise ValueError(msg)

        return trial

    def __del__(self) -> None:
        """Release the parent reference for GC."""
        self.api = None


class OptHub:
    """A class for accessing the OptHub public REST API."""

    client: raw.ApiClient
    poll_interval_sec = 0.5

    def __init__(self, api_key: str, host: str | None = None) -> None:
        """Creates an instance for API access from an API key."""
        conf = raw.Configuration(host=host)
        conf.api_key["ApiKeyAuth"] = api_key

        self.client = raw.ApiClient(conf)

    def match(self, uuid: str | UUID) -> Match:
        """Retrieve a match by its UUID."""
        match = Match()
        match.uuid = uuid if isinstance(uuid, UUID) else UUID(uuid)
        match.api = self

        return match

    def __enter__(self) -> Self:
        """A method to enable the use of the `with` statement."""
        self.client.__enter__()
        return self

    def __exit__(self, *args: object) -> None:
        """A method to enable the use of the `with` statement."""
        self.client.__exit__(*args)
