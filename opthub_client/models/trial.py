"""This module contains the types and functions related to participant trials."""

import asyncio
from typing import Any, Literal, TypedDict

from gql import gql

from opthub_client.errors.graphql_error import GraphQLError
from opthub_client.errors.query_error import QueryError
from opthub_client.graphql.client import execute_query, execute_query_async


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


def fetch_trial(match_id: str, trial_no: int) -> Trial | None:
    """Fetch the history of the user's submitted solution and their evaluation and score.

    Args:
        match_id (str): Match ID in the competition
        trial_no (int): Trial number

    Returns:
        Trial:
            The the history of the user's submitted solution and their evaluation and score.
    """
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
        result = execute_query(query, variables={"match": {"id": match_id}, "trialNo": trial_no})
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


def parse_fetched_trials(result: dict[str, Any], display_only_success: bool) -> tuple[list[Trial], bool, bool]:
    """Parse the fetched trials data.

    Args:
        result (Any|None): The fetched trials data
        display_only_success (bool): True to display only successful trials

    Returns:
        tuple[list[Trial], bool, bool]:
            The parsed trials, is_first, and is_last
    """
    data = result.get("getMatchTrialsByParticipant")
    if not isinstance(data, dict):
        raise QueryError(resource="trial", detail="Invalid data returned.")
    is_last = data.get("isLast", False)
    is_first = data.get("isFirst", False)
    trials = []
    for raw_trial in data.get("trials", []):
        trial = create_trial(raw_trial)
        if not display_only_success or trial.get("status") == "success":
            trials.append(trial)
    return trials, is_first, is_last


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
        limit (int): Size of the page
        trial_from (int): Trial number to start fetching
        is_asc (bool): True for show trials in ascending order, False for descending order
        display_only_success (bool): True to display only successful trials

    Returns:
        list[Trial]:
            The the history of the user's submitted solutions and their evaluations and scores.
    """
    return await fetch_trials_common(
        match_id,
        page,
        limit,
        trial_from,
        is_asc,
        display_only_success,
        is_async=True,
    )


def fetch_trials(
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
        limit (int): Size of the page
        trial_from (int): Trial number to start fetching
        is_asc (bool): True for show trials in ascending order, False for descending order
        display_only_success (bool): True to display only successful trials

    Returns:
        list[Trial]:
            The the history of the user's submitted solutions and their evaluations and scores.
    """
    return asyncio.run(
        fetch_trials_common(
            match_id,
            page,
            limit,
            trial_from,
            is_asc,
            display_only_success,
            is_async=False,
        ),
    )


async def fetch_trials_common(
    match_id: str,
    page: int,
    limit: int,
    trial_from: int,
    is_asc: bool,
    display_only_success: bool,
    is_async: bool,
) -> tuple[list[Trial], bool, bool]:
    """Common function to fetch the history of the user's submitted solutions and their evaluations and scores.

    Args:
        match_id (str): Match ID in the competition
        page (int): Page number
        limit (int): Size of the page
        trial_from (int): Trial number to start fetching
        is_asc (bool): True for show trials in ascending order, False for descending order
        display_only_success (bool): True to display only successful trials
        is_async (bool): True if calling asynchronously

    Returns:
        list[Trial]:
            The the history of the user's submitted solutions and their evaluations and scores.
    """
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
        if is_async:
            result = await execute_query_async(
                query,
                variables={
                    "match": {"id": match_id},
                    "range": {"startTrialNo": trial_from + 1 + page * limit, "limit": limit}
                    if is_asc
                    else {"endTrialNo": trial_from + -page * limit, "limit": limit},
                    "order": "ascending" if is_asc else "descending",
                },
            )
        else:
            loop = asyncio.get_event_loop()
            variables = {
                "match": {"id": match_id},
                "order": "ascending" if is_asc else "descending",
                "range": {
                    "startTrialNo": trial_from,
                    "limit": limit,
                },
            }
            if loop.is_running():
                result = await execute_query_async(
                    query,
                    variables=variables,
                )
            else:
                result = execute_query(
                    query,
                    variables=variables,
                )
    except GraphQLError as e:
        raise QueryError(resource="trial", detail=str(e.message)) from e
    return parse_fetched_trials(
        result=result,
        display_only_success=display_only_success,
    )


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
