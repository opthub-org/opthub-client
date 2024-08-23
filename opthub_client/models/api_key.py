"""This module contains the functions to create and get the API key from the server."""

from typing import TypedDict

from gql import gql

from opthub_client.errors.graphql_error import GraphQLError
from opthub_client.errors.query_error import QueryError
from opthub_client.graphql.client import execute_graphql


class ApiKey(TypedDict):
    """This class represents the API key type."""

    expires_at: str
    value: str


def create_api_key(force: bool) -> ApiKey:
    """Create and get API key from the server."""
    mutation = gql("""
        mutation createAPIKey(
        $force: Boolean
        ) {
            createAPIKey(
                force: $force
            ) {
                expiresAt
                value
            }
        }
    """)
    try:
        result = execute_graphql(mutation, variables={"force": force})
    except GraphQLError as e:
        raise QueryError(resource="api_key", detail=str(e.message)) from e
    data = result.get("createAPIKey")
    if not data:
        raise QueryError(resource="api_key", detail="No data returned from the server.")
    return ApiKey(expires_at=data.get("expiresAt"), value=data.get("value"))
