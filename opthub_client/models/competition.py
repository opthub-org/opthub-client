"""This module contains the functions related to competitions."""

import sys
from typing import TypedDict

import click
from gql import gql

from opthub_client.context.credentials import Credentials
from opthub_client.graphql.client import get_gql_client


class Competition(TypedDict):
    """This class represents the competition type."""

    id: str
    alias: str


def fetch_participated_competitions() -> list[Competition]:
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
                    id
                    alias
                }
            }
        }
        """)
    result = client.execute(query)
    data = result.get("getCompetitionsByParticipantUser")
    if data:
        participated_competitions = data.get("participating")
        if participated_competitions and isinstance(participated_competitions, list):
            return [Competition(id=comp["id"], alias=comp["alias"]) for comp in participated_competitions]
        # if no competitions found
        click.echo("No competitions found that you are participating in.")
        sys.exit(1)
    # if fetch failed
    error_message = "Failed to fetch participated competitions."
    raise ValueError(error_message)
