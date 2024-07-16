"""This module contains the functions related to competitions."""

from typing import TypedDict

from gql import gql

from opthub_client.errors.graphql_error import GraphQLError
from opthub_client.errors.query_error import QueryError
from opthub_client.graphql.client import execute_graphql


class Competition(TypedDict):
    """This class represents the competition type."""

    id: str
    alias: str


def fetch_participating_competitions() -> list[Competition]:
    """Fetch competitions and matches that the user is participating in.

    Args:
         uid (str): user ID
         username (str): user name
    Returns:
         list[Competition]: Competitions and matches that the user is participating in
    Raises:
        ValueError: If no competitions are found for the user or the fetch fails.
    """
    query = gql("""
        query getCompetitionsByParticipantUser(
        $id: String,
        $name: String
        ) {
            getCompetitionsByParticipantUser(
                id: $id,
                name: $name
            ) {
                participating {
                    id
                    alias
                }
            }
        }
        """)
    try:
        result = execute_graphql(query)
    except GraphQLError as e:
        raise QueryError(resource="competitions", detail=str(e)) from e
    data = result.get("getCompetitionsByParticipantUser")
    if not data:
        raise QueryError(resource="competitions", detail="No data returned.")
    participating_competitions = data.get("participating")
    if not isinstance(participating_competitions, list):
        raise QueryError(resource="competitions", detail="Invalid data returned.")
    return [Competition(id=comp["id"], alias=comp["alias"]) for comp in participating_competitions]
