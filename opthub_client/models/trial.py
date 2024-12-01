"""This module contains the types and functions related to participant trials."""

from typing import Any, Literal, TypedDict

from gql import gql
from graphql import DocumentNode

from opthub_client.errors.graphql_error import GraphQLError
from opthub_client.errors.query_error import QueryError
from opthub_client.graphql.client import execute_graphql, execute_graphql_async

TrialStatus = Literal["evaluating", "success", "scoring", "evaluator_failed", "scorer_failed"]


class Solution(TypedDict):
    """This class represents the solution type."""

    variable: str
    created_at: str


class Evaluation(TypedDict):
    """This class represents the evaluation type."""

    status: Literal["Success", "Failed"]
    objective: float | list[float]
    feasible: bool | None
    constraint: float | list[float]
    info: object
    started_at: str
    finished_at: str
    error: str | None


class Score(TypedDict):
    """This class represents the score type."""

    status: Literal["Success", "Failed"]
    value: float | None
    started_at: str | None
    finished_at: str | None
    error: str | None


class Trial(TypedDict):
    """This class represents the trial type."""

    trialNo: int
    solution: Solution
    status: TrialStatus
    evaluation: Evaluation | None
    score: Score | None


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
    if "evaluation" in trial_data and trial_data["evaluation"] is not None:
        evaluation = Evaluation(
            status=trial_data["evaluation"]["status"],
            objective=trial_data["evaluation"]["objective"],
            constraint=trial_data["evaluation"]["constraint"],
            feasible=trial_data["evaluation"]["feasible"],
            error=trial_data["evaluation"]["error"],
            info=trial_data["evaluation"]["info"],
            started_at=trial_data["evaluation"]["startedAt"],
            finished_at=trial_data["evaluation"]["finishedAt"],
        )
    score = None
    if "score" in trial_data and trial_data["score"] is not None:
        score = Score(
            status=trial_data["score"]["status"],
            value=trial_data["score"]["value"],
            started_at=trial_data["score"]["startedAt"],
            error=trial_data["score"]["error"],
            finished_at=trial_data["score"]["finishedAt"],
        )
    return Trial(
        trialNo=trial_data["trialNo"],
        solution=solution,
        status=status,
        evaluation=evaluation,
        score=score,
    )


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
                    error
                }
                score {
                    status
                    startedAt
                    finishedAt
                    value
                    error
                }
            }}""")
    try:
        result = execute_graphql(query, variables={"match": {"id": match_id}, "trialNo": trial_no})
    except GraphQLError as e:
        raise QueryError(resource="trial", detail=str(e.message)) from e
    if result is None:
        return None
    raw_trial = result.get("getMatchTrialByParticipant")
    if not raw_trial:
        return None
    if not isinstance(raw_trial, dict):
        raise QueryError(resource="trial", detail="Invalid data returned.")
    trial = create_trial(raw_trial)
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


def make_fetch_trials_query_document() -> DocumentNode:
    """Make the graphql document node to fetch the trials.

    Returns:
        DocumentNode:
            The graphql document node to fetch the trials.
    """
    return gql("""
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
                        error
                        info
                    }
                    score {
                        status
                        startedAt
                        finishedAt
                        value
                        error
                    }
                }
            }}""")


def make_fetch_trials_query_variables(
    match_id: str,
    page: int,
    page_size: int,
    limit: int,
    offset: int,
    is_asc: bool,
) -> dict[str, Any]:
    """Make the variables for the fetch trials query.

    Args:
        match_id (str): Match ID in the competition
        page (int): Page number
        page_size(int): Size of the page
        limit (int): Size of the page
        offset (int): Trial number to start fetching
        is_asc (bool): True for show trials in ascending order, False for descending order

    Returns:
         dict[str, Any]:
            The variables for the fetch trials query.
    """
    return {
        "match": {"id": match_id},
        "range": {"startTrialNo": offset + page * page_size, "limit": limit}
        if is_asc
        else {"endTrialNo": offset - page * page_size, "limit": limit},
        "order": "ascending" if is_asc else "descending",
    }


async def fetch_trials_async(
    match_id: str,
    page: int,
    page_size: int,
    limit: int,
    offset: int,
    is_asc: bool,
    display_only_success: bool,
) -> tuple[list[Trial], bool, bool]:
    """Fetch the history of the user's submitted solutions and their evaluations and scores.

    Args:
        match_id (str): Match ID in the competition
        page (int): Page number
        page_size(int): Size of the page
        limit (int): Size of the page
        offset (int): Trial number to start fetching
        is_asc (bool): True for show trials in ascending order, False for descending order
        display_only_success (bool): True to display only successful trials

    Returns:
        list[Trial]:
            The history of the user's submitted solutions and their evaluations and scores.
    """
    query = make_fetch_trials_query_document()
    variables = make_fetch_trials_query_variables(match_id, page, page_size, limit, offset, is_asc)
    try:
        result = await execute_graphql_async(query, variables)
    except GraphQLError as e:
        raise QueryError(resource="trial", detail=str(e.message)) from e
    return parse_fetched_trials(result, display_only_success)


def fetch_trials(
    match_id: str,
    page: int,
    page_size: int,
    limit: int,
    offset: int,
    is_asc: bool,
    display_only_success: bool,
) -> tuple[list[Trial], bool, bool]:
    """Fetch the history of the user's submitted solutions and their evaluations and scores.

    Args:
        match_id (str): Match ID in the competition
        page (int): Page number
        page_size(int): Size of the page
        limit (int): Size of the page
        offset (int): Trial number to start fetching
        is_asc (bool): True for show trials in ascending order, False for descending order
        display_only_success (bool): True to display only successful trials

    Returns:
        list[Trial]:
            The the history of the user's submitted solutions and their evaluations and scores.
    """
    query = make_fetch_trials_query_document()
    variables = make_fetch_trials_query_variables(match_id, page, page_size, limit, offset, is_asc)
    try:
        result = execute_graphql(query, variables)
    except GraphQLError as e:
        raise QueryError(resource="trial", detail=str(e.message)) from e
    return parse_fetched_trials(result, display_only_success)
