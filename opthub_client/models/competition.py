"""This module contains the functions related to competitions."""

import sys
from typing import TypedDict

import click
from gql import gql

from opthub_client.errors.graphql_error import GraphQLError
from opthub_client.errors.query_error import QueryError
from opthub_client.graphql.client import execute_query, get_gql_client


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
    try:
        result = execute_query(client, query)
        data = result.get("getCompetitionsByParticipantUser")
        if data:
            participating_competitions = data.get("participating")
            if participating_competitions and isinstance(participating_competitions, list):
                return [Competition(id=comp["id"], alias=comp["alias"]) for comp in participating_competitions]
            # if no competitions found
            click.echo("No competitions found that you are participating in.")
            sys.exit(1)
        raise QueryError(resource="competitions", detail="No data returned.")
    except GraphQLError as e:
        raise QueryError(resource="competitions", detail=str(e.message)) from e
