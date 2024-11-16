"""Access to the OptHub public REST API.

The module is designed to wrap a library that is automatically generated from the OpenAPI schema
to access the OptHub public REST API.

The automatically generated raw Python package is available at https://github.com/opthub-org/opthub-api-client-python.
"""

from __future__ import annotations

import time
from random import random
from time import sleep
from typing import TYPE_CHECKING, NamedTuple, TypeVar
from uuid import UUID

import numpy as np
import opthub_api_client as raw
from opthub_api_client import MatchTrialEvaluation, MatchTrialScore, MatchTrialStatus, Solution

if TYPE_CHECKING:
    from collections.abc import Callable

    from numpy.typing import ArrayLike

T = TypeVar("T")
TOptHub = TypeVar("TOptHub", bound="OptHub")

__all__ = [
    "raw",
    "OptHub",
    "Match",
    "TrialStatus",
    "Trial",
    "MatchTrialStatus",
    "MatchTrialEvaluation",
    "MatchTrialScore",
    "Solution",
    "EvaluationError",
    "ScoringError",
]


class TrialStatus(NamedTuple):
    """A record representing the result of trial status retrieval."""

    type: MatchTrialStatus


class EvaluationError(Exception):
    """Exception during evaluation calculation failure."""


class ScoringError(Exception):
    """Exception during score calculation failure."""


class Trial:
    """A class representing the match trial."""

    trial_no: int
    status: TrialStatus
    evaluation: MatchTrialEvaluation | None
    score: MatchTrialScore | None
    match: Match

    def wait_evaluation(self, timeout: float | None = None) -> MatchTrialEvaluation:
        """Wait until the evaluation is complete, then return the results."""
        self._poll(
            lambda: self.update_status(),
            lambda _: self.status.type != MatchTrialStatus.EVALUATING,
            timeout,
            first_wait=False,
        )

        self.evaluation = raw.MatchTrialsApi(self.match.api.client).get_match_evaluation(
            str(self.match.uuid),
            self.trial_no,
        )

        if self.evaluation.error is not None:
            raise EvaluationError(self.evaluation.error)

        return self.evaluation

    def wait_scoring(self, timeout: float | None = None) -> MatchTrialScore:
        """Wait until the scoring is complete, then return the results."""
        self._poll(
            lambda: self.update_status(),
            lambda _: self.status.type not in {MatchTrialStatus.EVALUATING, MatchTrialStatus.SCORING},
            timeout,
            first_wait=False,
        )

        self.score = raw.MatchTrialsApi(self.match.api.client).get_match_score(
            str(self.match.uuid),
            self.trial_no,
        )

        if self.score.error is not None:
            raise ScoringError(self.score.error)

        return self.score

    def get_solution(self) -> Solution:
        """Retrieves a past submitted solution."""
        return raw.MatchTrialsApi(self.match.api.client).get_solution(str(self.match.uuid), self.trial_no)

    def update_status(self) -> None:
        """Retrieves the status of the trial.

        Wait until the submitted results are reflected on the server side and the trial information becomes available.
        """
        trial = self._poll(
            lambda: self.match.try_get_trial(self.trial_no),
            lambda trial: trial is not None,
            None,
            first_wait=False,
        )
        self.status = trial.status

    def _poll(
        self,
        callback: Callable[[], T],
        finish_condition: Callable[[T], bool],
        timeout: float | None,
        first_wait: bool,
    ) -> T:
        """Perform polling based on exponential backoff."""
        start = time.time()
        api = self.match.api
        wait_sec = api.poll_interval_initial_sec

        def wait() -> None:
            nonlocal wait_sec
            sleep(wait_sec + random() * api.poll_max_random_delay_sec)  # noqa: S311
            wait_sec = min(wait_sec * api.poll_exponential_backoff_ratio, api.poll_interval_max_sec)

        if first_wait:
            wait()

        while True:
            result = callback()
            if finish_condition(result):
                return result

            if timeout is not None and (time.time() - start) > timeout:
                raise TimeoutError

            wait()

    def __del__(self) -> None:
        """Release the parent reference for GC."""
        self.match = None


class Match:
    """A class representing a match in a competition."""

    uuid: UUID
    api: OptHub

    def submit(self, solution: ArrayLike) -> Trial:
        """Submit a solution."""
        array = np.array(solution, dtype=np.double)
        variable = {"scalar": array[0]} if array.ndim == 0 else {"vector": array}

        response = raw.MatchTrialsApi(self.api.client).create_match_trial(str(self.uuid), {"variable": variable})

        trial = Trial()
        trial.trial_no = response.trial_no
        trial.status = TrialStatus(response.status)
        trial.evaluation = None
        trial.score = None
        trial.match = self
        return trial

    def try_get_trial(self, trial_no: int) -> Trial | None:
        """Retrieves the status of the trial with the specified trial number.

        If the corresponding trial number does not exist, it returns `None`.
        """
        try:
            response = raw.MatchTrialsApi(self.api.client).get_match_trial(str(self.uuid), trial_no)

            status = TrialStatus(response.status)

            trial = Trial()
            trial.trial_no = trial_no
            trial.status = status
            trial.evaluation = None
            trial.score = None
            trial.match = self

        except raw.exceptions.NotFoundException as e:
            if e.body["code"] == "TrialNotFound":
                return None
            raise

        return trial

    def get_trial(self, trial_no: int) -> Trial:
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
    poll_interval_initial_sec = 0.5
    poll_interval_max_sec = 5 * 60
    poll_max_random_delay_sec = 0.5
    poll_exponential_backoff_ratio = 1.2

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

    def __enter__(self) -> TOptHub:
        """A method to enable the use of the `with` statement."""
        self.client.__enter__()
        return self

    def __exit__(self, *args: object) -> None:
        """A method to enable the use of the `with` statement."""
        self.client.__exit__(*args)
