"""This module contains the types and functions related to participant trials."""

from typing import Any, Literal, TypedDict

from gql import gql

from opthub_client.errors.graphql_error import GraphQLError
from opthub_client.errors.query_error import QueryError
from opthub_client.graphql.client import execute_query, execute_query_async, get_gql_client


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


async def fetch_trials_async(
    match_id: str,
    page: int,
    limit: int,
    trial_from: int,
    is_asc: bool,
    display_only_success: bool,
) -> tuple[list[Trial], bool, bool]:
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
    try:
        result = await execute_query_async(
            client,
            query,
            variables={
                "match": {"id": match_id},
                "range": {"startTrialNo": trial_from + 1 + page * limit, "limit": limit}
                if is_asc
                else {"endTrialNo": trial_from + -page * limit, "limit": limit},
                "order": "ascending" if is_asc else "descending",
            },
        )
    except GraphQLError as e:
        raise QueryError(resource="trial", detail=str(e.message)) from e
    if result is None:
        return [], False, False
    data = result.get("getMatchTrialsByParticipant")
    trials = []
    is_first = False
    is_last = False
    if not data:
        return [], False, False
    if not isinstance(data, dict):
        raise QueryError(resource="trial", detail="Invalid data returned.")
    is_first = data.get("isFirst", False)
    is_last = data.get("isLast", False)
    trials_data = data.get("trials", [])
    for trial_data in trials_data:
        trial = create_trial(trial_data)
        if not display_only_success or trial.get("status") == "success":
            trials.append(trial)
    return trials, is_first, is_last


def fetch_trials(
    match_id: str,
    start: int,
    limit: int,
    is_desc: bool,
    display_only_success: bool,
) -> tuple[list[Trial], bool, bool]:
    """Fetch the history of the user's submitted solutions and their evaluations and scores.

    Args:
        match_id (str): Match ID in the competition
        start (int): Trial number to start fetching
        limit (int): Number of trials to fetch
        display_only_success (bool): True to display only successful trials
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
    try:
        result = execute_query(
            client,
            query,
            variables={
                "match": {"id": match_id},
                "order": "descending" if is_desc else "ascending",
                "range": {
                    "startTrialNo": start,
                    "limit": limit,
                },
            },
        )
    except GraphQLError as e:
        raise QueryError(resource="trial", detail=str(e.message)) from e
    if result is None:
        return []
    data = result.get("getMatchTrialsByParticipant")
    trials = []
    is_last = False
    is_first = False
    if not data:
        return [], False, False
    if not isinstance(data, dict):
        raise QueryError(resource="trial", detail="Invalid data returned.")
    trials_data = data.get("trials", [])
    is_last = data.get("isLast", False)
    is_first = data.get("isFirst", False)
    for trial_data in trials_data:
        trial = create_trial(trial_data)
        if not display_only_success or trial.get("status") == "success":
            trials.append(trial)
    return trials, is_first, is_last


def fetch_trial(match_id: str, trial_no: int) -> Trial | None:
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
            query getMatchTrialByParticipant(
            $match: MatchIdentifierInput!,
            $trialNo: Int!
            ) {
            getMatchTrialByParticipant(
                match: $match,
                trialNo: $trialNo
            ) {
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
            }}""")
    try:
        result = execute_query(client, query, variables={"match": {"id": match_id}, "trialNo": trial_no})
    except GraphQLError as e:
        raise QueryError(resource="trial", detail=str(e.message)) from e
    if result is None:
        return None
    trial_data = result.get("getMatchTrialByParticipant")
    if not trial_data:
        return None
    if not isinstance(trial_data, dict):
        raise QueryError(resource="trial", detail="Invalid data returned.")
    trial = create_trial(trial_data)
    return trial


def create_trial(trial_data: dict[str, Any]) -> Trial:
    """Create a Trial object from trial data.

    Args:
        trial_data (dict[str, Any]): trail data from the server

    Returns:
        Trial: the trial object
    """
    status = trial_data.get("status", "evaluating")
    solution = Solution(
        variable=trial_data["solution"]["variable"],
        created_at=trial_data["solution"]["createdAt"],
    )
    evaluation = None
    if status in ("success", "scoring", "scorer_failed") and "evaluation" in trial_data:
        evaluation = Evaluation(
            status=trial_data["evaluation"]["status"],
            objective=trial_data["evaluation"]["objective"],
            constraint=trial_data["evaluation"]["constraint"],
            info=trial_data["evaluation"]["info"],
            started_at=trial_data["evaluation"]["startedAt"],
            finished_at=trial_data["evaluation"]["finishedAt"],
        )
    score = None
    if status in ("success") and "score" in trial_data:
        score = Score(
            status=trial_data["score"]["status"],
            score=trial_data["score"]["value"],
            started_at=trial_data["score"]["startedAt"],
            finished_at=trial_data["score"]["finishedAt"],
        )
    return Trial(
        trialNo=trial_data["trialNo"],
        solution=solution,
        status=status,
        evaluation=evaluation,
        score=score,
    )
