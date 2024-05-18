"""This module contains the types and functions related to participant trials."""

from typing import Literal, TypedDict


class Solution(TypedDict):
    """This class represents the solution type."""

    variable: str
    created_at: str


class Evaluation(TypedDict):
    """This class represents the evaluation type."""

    status: Literal["waiting", "success", "failed"]
    objective: float | list[float]
    constraint: float | list[float]
    info: object
    started_at: str
    finished_at: str


class Score(TypedDict):
    """This class represents the score type."""

    status: Literal["waiting", "success", "failed"]
    score: float | None
    started_at: str | None
    finished_at: str | None


class Trial(TypedDict):
    """This class represents the trial type."""

    trialNo: int
    solution: Solution
    evaluation: Evaluation
    score: Score


def fetch_trials(competition_id: str, match_id: str, page: int, size: int) -> list[Trial]:
    """Fetch the history of the user's submitted solutions and their evaluations and scores.

    Args:
        competition_id (str): Competition ID
        match_id (str): Match ID in the competition
        page (int): Page number
        size (int): Size of the page

    Returns:
        list[Trial]:
            The the history of the user's submitted solutions and their evaluations and scores.
    """
    trials: list[Trial] = [
        {
            "trialNo": 1,
            "solution": {
                "variable": "3.0",
                "created_at": "2021-01-01",
            },
            "evaluation": {
                "objective": 3.0,
                "constraint": 4.0,
                "info": {},
                "status": "success",
                "started_at": "2021-01-01",
                "finished_at": "2021-01-01",
            },
            "score": {
                "score": 3.2,
                "status": "success",
                "started_at": "2021-01-01",
                "finished_at": "2021-01-01",
            },
        },
    ]
    return trials
