"""This module contains the functions related to matches."""

from typing import TypedDict

from gql import gql

from opthub_client.errors.graphql_error import GraphQLError
from opthub_client.errors.query_error import QueryError
from opthub_client.graphql.client import execute_query, get_gql_client


class Match(TypedDict):
    """This class represents the match type."""

    id: str
    alias: str


def fetch_matches_by_competition(comp_id: str, comp_alias: str) -> list[Match]:
    """Fetch matches by competition alias.

    Args:
        comp_id (str): Competition ID
        comp_alias (str): Competition alias

    Returns:
        list[Match]: Matches related to the competition
    """
    client = get_gql_client()
    query = gql("""
        query getMatchesByCompetition(
        $id: String,
        $alias: String
        ) {
        getMatchesByCompetition(
            id: $id,
            alias: $alias
        ) {
            id
            competition {
                id
                alias
            }
            problem {
                id
                alias
            }
            indicator {
                id
                alias
            }
            alias
            successTrialsBudget
            submissionsBudget
            isTutorial
            problemPublicEnvironments {
                key
                value
            }
            indicatorPublicEnvironments {
                key
                value
            }
            problemPrivateEnvironments {
                key
                value
            }
            indicatorPrivateEnvironments {
                key
                value
            }
            openAt
            closeAt
        }
        }""")
    try:
        result = execute_query(client, query, variables={"id": comp_id, "alias": comp_alias})
        data = result.get("getMatchesByCompetition")
        if data and isinstance(data, list):
            return [Match(id=match["id"], alias=match["alias"]) for match in data]
        raise QueryError(resource="matches", detail="No data returned.")
    except GraphQLError as e:
        raise QueryError(resource="matches", detail=str(e.message)) from e
