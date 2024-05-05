"""This module contains the functions related to competitions."""

from typing import TypedDict

from gql import gql

from opthub_client.graphql.client import get_gql_client


class Competition(TypedDict):
    """This class represents the competition type."""

    id: str
    alias: str


def fetch_participated_competitions(uid: str, username: str) -> list[Competition]:
    """Fetch competitions and matches that the user is participating in.

    Args:
         uid (str): user ID
         username (str): user name
    Returns:
         list[Competition]: Competitions and matches that the user is participating in
    Raises:
        ValueError: If no competitions are found for the user or the fetch fails.
    """
    client = get_gql_client()
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
            ...CompetitionFragment
            }
            participated {
            ...CompetitionFragment
            }
        }
        }""")
    result = client.execute(query, variable_values={"id": uid, "alias": username})
    data = result.get("getCompetitionsByParticipantUser")
    if data and data.get("participating") and isinstance(data.get("participating"), list):
        return [Competition(id=comp["id"], alias=comp["alias"]) for comp in data.get("participating")]
    error_message = "Failed to fetch participated competitions."
    raise ValueError(error_message)
