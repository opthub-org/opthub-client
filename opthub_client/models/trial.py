"""This module contains the types and functions related to participant trials."""

from typing import Literal, TypedDict

from gql import gql

from opthub_client.graphql.client import get_gql_client


class Solution(TypedDict):
    """This class represents the solution type."""

    variable: str
    created_at: str


class Evaluation(TypedDict):
    """This class represents the evaluation type."""

    status: Literal["Success", "Failed"]
    objective: float | list[float]
    constraint: float | list[float]
    info: object
    started_at: str
    finished_at: str


class Score(TypedDict):
    """This class represents the score type."""

    status: Literal["Success", "Failed"]
    score: float | None
    started_at: str | None
    finished_at: str | None


class Trial(TypedDict):
    """This class represents the trial type."""

    trialNo: int
    solution: Solution
    status: Literal["evaluating", "success", "scoring", "evaluator_failed", "scorer_failed"]
    evaluation: Evaluation | None
    score: Score | None


async def fetch_trials_async(match_id: str, page: int, size: int, asc: bool) -> tuple[list[Trial], bool, bool]:
    """Fetch the history of the user's submitted solutions and their evaluations and scores.

    Args:
        match_id (str): Match ID in the competition
        page (int): Page number
        size (int): Size of the page
        asc (bool): True for show trials in ascending order, False for descending order

    Returns:
        list[Trial]:
            The the history of the user's submitted solutions and their evaluations and scores.
    """
    client = get_gql_client()
    query = gql("""
            query getMatchTrialsByParticipant(
            $match: MatchIdentifierInput!,
            $participant: ParticipantInput,
            $range: MatchTrialsRangeInput,
            $order: Order
            ) {
            getMatchTrialsByParticipant(
                match: $match,
                participant: $participant,
                range: $range,
                order: $order
            ) {
                isFirst
                isLast
                startTrialNo
                endTrialNo
                trials {
                    trialNo
                    status
                    solution {
                        variable
                        createdAt
                    }
                    evaluation {
                        constraint
                        feasible
                        objective
                        status
                        startedAt
                        finishedAt
                        info
                    }
                    score {
                        status
                        startedAt
                        finishedAt
                        value
                    }
                }
            }}""")
    result = await client.execute_async(
        query,
        variable_values={
            "match": {"id": match_id},
            "range": {"startTrialNo": page * size + 1, "limit": size - 1}
            if asc
            else {"endTrialNo": -page * size, "limit": size - 1},
            "order": "ascending" if asc else "descending",
        },
    )
    if result is None:
        return [], False, False
    data = result.get("getMatchTrialsByParticipant")
    trials = []
    is_first = False
    is_last = False
    if data and isinstance(data, dict):
        is_first = data.get("isFirst")
        is_last = data.get("isLast")
        trials_data = data.get("trials", [])
        for trial_data in trials_data:
            if trial_data.get("status") == "success":
                evaluation = Evaluation(
                    status=trial_data["evaluation"]["status"],
                    objective=trial_data["evaluation"]["objective"],
                    constraint=trial_data["evaluation"]["constraint"],
                    info=trial_data["evaluation"]["info"],
                    started_at=trial_data["evaluation"]["startedAt"],
                    finished_at=trial_data["evaluation"]["finishedAt"],
                )
                score = Score(
                    status=trial_data["score"]["status"],
                    score=trial_data["score"]["value"],
                    started_at=trial_data["score"]["startedAt"],
                    finished_at=trial_data["score"]["finishedAt"],
                )
                solution = Solution(
                    variable=trial_data["solution"]["variable"],
                    created_at=trial_data["solution"]["createdAt"],
                )
                trial = Trial(
                    trialNo=trial_data["trialNo"],
                    solution=solution,
                    status=trial_data["status"],
                    evaluation=evaluation,
                    score=score,
                )
                trials.append(trial)
            elif trial_data.get("status") == "evaluating":
                solution = Solution(
                    variable=trial_data["solution"]["variable"],
                    created_at=trial_data["solution"]["createdAt"],
                )
                trial = Trial(
                    trialNo=trial_data["trialNo"],
                    solution=solution,
                    status=trial_data["status"],
                    evaluation=None,
                    score=None,
                )
                trials.append(trial)
            elif trial_data.get("status") == "scoring":
                evaluation = Evaluation(
                    status=trial_data["evaluation"]["status"],
                    objective=trial_data["evaluation"]["objective"],
                    constraint=trial_data["evaluation"]["constraint"],
                    info=trial_data["evaluation"]["info"],
                    started_at=trial_data["evaluation"]["startedAt"],
                    finished_at=trial_data["evaluation"]["finishedAt"],
                )
                solution = Solution(
                    variable=trial_data["solution"]["variable"],
                    created_at=trial_data["solution"]["createdAt"],
                )
                trial = Trial(
                    trialNo=trial_data["trialNo"],
                    solution=solution,
                    status=trial_data["status"],
                    evaluation=evaluation,
                    score=None,
                )
                trials.append(trial)
            elif trial_data.get("status") == "scorer_failed":
                solution = Solution(
                    variable=trial_data["solution"]["variable"],
                    created_at=trial_data["solution"]["createdAt"],
                )
                evaluation = Evaluation(
                    status=trial_data["evaluation"]["status"],
                    objective=trial_data["evaluation"]["objective"],
                    constraint=trial_data["evaluation"]["constraint"],
                    info=trial_data["evaluation"]["info"],
                    started_at=trial_data["evaluation"]["startedAt"],
                    finished_at=trial_data["evaluation"]["finishedAt"],
                )
                trial = Trial(
                    trialNo=trial_data["trialNo"],
                    solution=solution,
                    status=trial_data["status"],
                    evaluation=evaluation,
                    score=None,
                )
                trials.append(trial)
            elif trial_data.get("status") == "evaluator_failed":
                solution = Solution(
                    variable=trial_data["solution"]["variable"],
                    created_at=trial_data["solution"]["createdAt"],
                )
                trial = Trial(
                    trialNo=trial_data["trialNo"],
                    solution=solution,
                    status=trial_data["status"],
                    evaluation=None,
                    score=None,
                )
                trials.append(trial)
            else:
                raise AssertionError("Unknown trial status")
    return trials, is_first, is_last


def fetch_trials(match_id: str, size: int, trial_no: int) -> list[Trial]:
    """Fetch the history of the user's submitted solutions and their evaluations and scores.

    Args:
        match_id (str): Match ID in the competition
        size (int): Size of fetch trials
        trial_no (int): Trial number to start fetching

    Returns:
        list[Trial]:
            The the history of the user's submitted solutions and their evaluations and scores.
    """
    client = get_gql_client()
    query = gql("""
            query getMatchTrialsByParticipant(
            $match: MatchIdentifierInput!,
            $participant: ParticipantInput,
            $range: MatchTrialsRangeInput,
            $order: Order
            ) {
            getMatchTrialsByParticipant(
                match: $match,
                participant: $participant,
                range: $range,
                order: $order
            ) {
                startTrialNo
                endTrialNo
                trials {
                    trialNo
                    status
                    solution {
                        variable
                        createdAt
                    }
                    evaluation {
                        constraint
                        feasible
                        objective
                        status
                        startedAt
                        finishedAt
                        info
                    }
                    score {
                        status
                        startedAt
                        finishedAt
                        value
                    }
                }
            }}""")
    result = client.execute(
        query,
        variable_values={"match": {"id": match_id}, "range": {"startTrialNo": trial_no, "limit": size - 1}},
    )
    if result is None:
        return []
    data = result.get("getMatchTrialsByParticipant")
    trials = []
    if data and isinstance(data, dict):
        trials_data = data.get("trials", [])
        for trial_data in trials_data:
            if trial_data.get("status") == "success":
                evaluation = Evaluation(
                    status=trial_data["evaluation"]["status"],
                    objective=trial_data["evaluation"]["objective"],
                    constraint=trial_data["evaluation"]["constraint"],
                    info=trial_data["evaluation"]["info"],
                    started_at=trial_data["evaluation"]["startedAt"],
                    finished_at=trial_data["evaluation"]["finishedAt"],
                )
                score = Score(
                    status=trial_data["score"]["status"],
                    score=trial_data["score"]["value"],
                    started_at=trial_data["score"]["startedAt"],
                    finished_at=trial_data["score"]["finishedAt"],
                )
                solution = Solution(
                    variable=trial_data["solution"]["variable"],
                    created_at=trial_data["solution"]["createdAt"],
                )
                trial = Trial(
                    trialNo=trial_data["trialNo"],
                    solution=solution,
                    status=trial_data["status"],
                    evaluation=evaluation,
                    score=score,
                )
                trials.append(trial)
            elif trial_data.get("status") == "evaluating":
                solution = Solution(
                    variable=trial_data["solution"]["variable"],
                    created_at=trial_data["solution"]["createdAt"],
                )
                trial = Trial(
                    trialNo=trial_data["trialNo"],
                    solution=solution,
                    status=trial_data["status"],
                    evaluation=None,
                    score=None,
                )
                trials.append(trial)
            elif trial_data.get("status") == "scoring":
                evaluation = Evaluation(
                    status=trial_data["evaluation"]["status"],
                    objective=trial_data["evaluation"]["objective"],
                    constraint=trial_data["evaluation"]["constraint"],
                    info=trial_data["evaluation"]["info"],
                    started_at=trial_data["evaluation"]["startedAt"],
                    finished_at=trial_data["evaluation"]["finishedAt"],
                )
                solution = Solution(
                    variable=trial_data["solution"]["variable"],
                    created_at=trial_data["solution"]["createdAt"],
                )
                trial = Trial(
                    trialNo=trial_data["trialNo"],
                    solution=solution,
                    status=trial_data["status"],
                    evaluation=evaluation,
                    score=None,
                )
                trials.append(trial)
            elif trial_data.get("status") == "scorer_failed":
                solution = Solution(
                    variable=trial_data["solution"]["variable"],
                    created_at=trial_data["solution"]["createdAt"],
                )
                evaluation = Evaluation(
                    status=trial_data["evaluation"]["status"],
                    objective=trial_data["evaluation"]["objective"],
                    constraint=trial_data["evaluation"]["constraint"],
                    info=trial_data["evaluation"]["info"],
                    started_at=trial_data["evaluation"]["startedAt"],
                    finished_at=trial_data["evaluation"]["finishedAt"],
                )
                trial = Trial(
                    trialNo=trial_data["trialNo"],
                    solution=solution,
                    status=trial_data["status"],
                    evaluation=evaluation,
                    score=None,
                )
                trials.append(trial)
            elif trial_data.get("status") == "evaluator_failed":
                solution = Solution(
                    variable=trial_data["solution"]["variable"],
                    created_at=trial_data["solution"]["createdAt"],
                )
                trial = Trial(
                    trialNo=trial_data["trialNo"],
                    solution=solution,
                    status=trial_data["status"],
                    evaluation=None,
                    score=None,
                )
                trials.append(trial)
            else:
                raise AssertionError("Unknown trial status")
    return trials


def fetch_trial(match_id: str, trial_no: int) -> Trial:
    """Fetch the history of the user's submitted solution and their evaluation and score.

    Args:
        match_id (str): Match ID in the competition
        trial_no (int): Trial number

    Returns:
        Trial:
            The the history of the user's submitted solution and their evaluation and score.
    """
    client = get_gql_client()
    query = gql("""
            query getMatchTrialsByParticipant(
            $match: MatchIdentifierInput!,
            $participant: ParticipantInput,
            $range: MatchTrialsRangeInput,
            $order: Order
            ) {
            getMatchTrialsByParticipant(
                match: $match,
                participant: $participant,
                range: $range,
                order: $order
            ) {
                startTrialNo
                endTrialNo
                trials {
                    trialNo
                    status
                    solution {
                        variable
                        createdAt
                    }
                    evaluation {
                        constraint
                        feasible
                        objective
                        status
                        startedAt
                        finishedAt
                        info
                    }
                    score {
                        status
                        startedAt
                        finishedAt
                        value
                    }
                }
            }}""")
    result = client.execute(
        query,
        variable_values={"match": {"id": match_id}, "range": {"endTrialNo": trial_no, "limit": 1}},
    )
    if result is None:
        return None
    data = result.get("getMatchTrialsByParticipant")
    if data and isinstance(data, dict):
        trials_data = data.get("trials", [])
        for trial_data in trials_data:
            if trial_data.get("status") == "success":
                evaluation = Evaluation(
                    status=trial_data["evaluation"]["status"],
                    objective=trial_data["evaluation"]["objective"],
                    constraint=trial_data["evaluation"]["constraint"],
                    info=trial_data["evaluation"]["info"],
                    started_at=trial_data["evaluation"]["startedAt"],
                    finished_at=trial_data["evaluation"]["finishedAt"],
                )
                score = Score(
                    status=trial_data["score"]["status"],
                    score=trial_data["score"]["value"],
                    started_at=trial_data["score"]["startedAt"],
                    finished_at=trial_data["score"]["finishedAt"],
                )
                solution = Solution(
                    variable=trial_data["solution"]["variable"],
                    created_at=trial_data["solution"]["createdAt"],
                )
                trial = Trial(
                    trialNo=trial_data["trialNo"],
                    solution=solution,
                    status=trial_data["status"],
                    evaluation=evaluation,
                    score=score,
                )
            elif trial_data.get("status") == "evaluating":
                solution = Solution(
                    variable=trial_data["solution"]["variable"],
                    created_at=trial_data["solution"]["createdAt"],
                )
                trial = Trial(
                    trialNo=trial_data["trialNo"],
                    solution=solution,
                    status=trial_data["status"],
                    evaluation=None,
                    score=None,
                )
            elif trial_data.get("status") == "scoring":
                evaluation = Evaluation(
                    status=trial_data["evaluation"]["status"],
                    objective=trial_data["evaluation"]["objective"],
                    constraint=trial_data["evaluation"]["constraint"],
                    info=trial_data["evaluation"]["info"],
                    started_at=trial_data["evaluation"]["startedAt"],
                    finished_at=trial_data["evaluation"]["finishedAt"],
                )
                solution = Solution(
                    variable=trial_data["solution"]["variable"],
                    created_at=trial_data["solution"]["createdAt"],
                )
                trial = Trial(
                    trialNo=trial_data["trialNo"],
                    solution=solution,
                    status=trial_data["status"],
                    evaluation=evaluation,
                    score=None,
                )
            elif trial_data.get("status") == "scorer_failed":
                solution = Solution(
                    variable=trial_data["solution"]["variable"],
                    created_at=trial_data["solution"]["createdAt"],
                )
                evaluation = Evaluation(
                    status=trial_data["evaluation"]["status"],
                    objective=trial_data["evaluation"]["objective"],
                    constraint=trial_data["evaluation"]["constraint"],
                    info=trial_data["evaluation"]["info"],
                    started_at=trial_data["evaluation"]["startedAt"],
                    finished_at=trial_data["evaluation"]["finishedAt"],
                )
                trial = Trial(
                    trialNo=trial_data["trialNo"],
                    solution=solution,
                    status=trial_data["status"],
                    evaluation=evaluation,
                    score=None,
                )
            elif trial_data.get("status") == "evaluator_failed":
                solution = Solution(
                    variable=trial_data["solution"]["variable"],
                    created_at=trial_data["solution"]["createdAt"],
                )
                trial = Trial(
                    trialNo=trial_data["trialNo"],
                    solution=solution,
                    status=trial_data["status"],
                    evaluation=None,
                    score=None,
                )
            else:
                raise AssertionError("Unknown trial status")
    return trial
