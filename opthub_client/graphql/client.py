"""This module contains the GraphQL client getter."""

from typing import Any

from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError
from graphql import DocumentNode

from opthub_client.context.credentials import Credentials
from opthub_client.errors.graphql_error import GraphQLError

URL = "https://jciqso7l7rhajfkt5s3dhybpcu.appsync-api.ap-northeast-1.amazonaws.com/graphql"


def execute_query(query: DocumentNode, variables: dict[str, Any] | None = None) -> dict[str, Any]:
    """Execute a query.

    Args:
        client (Client): graphql client
        query (DocumentNode): query
        variables (_type_, optional): query variables. Defaults to None.

    Raises:
        GraphQLError: graphql error

    Returns:
        dict[str, Any]: result
    """
    credentials = Credentials()
    credentials.load()
    headers = {"Authorization": f"Bearer {credentials.access_token}"}
    transport = AIOHTTPTransport(url=URL, headers=headers)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    try:
        return client.execute(query, variable_values=variables)
    except TransportQueryError as auth_error:
        error_message = auth_error.errors[0]["message"] if auth_error.errors else "Unexpected error"
        raise GraphQLError(message=error_message) from auth_error


async def execute_query_async(
    query: DocumentNode,
    variables: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Execute a query asynchronously.

    Args:
        client (Client): graphql client
        query (DocumentNode): query
        variables (_type_, optional): query variables. Defaults to None.

    Raises:
        GraphQLError: graphql error

    Returns:
        dict[str, Any]: result
    """
    credentials = Credentials()
    credentials.load()
    headers = {"Authorization": f"Bearer {credentials.access_token}"}
    transport = AIOHTTPTransport(url=URL, headers=headers)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    try:
        return await client.execute_async(query, variable_values=variables)
    except TransportQueryError as auth_error:
        error_message = auth_error.errors[0]["message"] if auth_error.errors else "Unexpected error"
        raise GraphQLError(message=error_message) from auth_error


def execute_mutation(
    mutation: DocumentNode,
    variables: dict[str, Any] | None = None,
) -> None:
    """Execute a mutation.

    Args:
        client (Client): graphql client
        mutation (DocumentNode): mutation
        variables (_type_, optional): mutation variables. Defaults to None.

    Raises:
        GraphQLError: graphql error
    """
    credentials = Credentials()
    credentials.load()
    headers = {"Authorization": f"Bearer {credentials.access_token}"}
    transport = AIOHTTPTransport(url=URL, headers=headers)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    try:
        client.execute(mutation, variables)
    except TransportQueryError as auth_error:
        error_message = auth_error.errors[0]["message"] if auth_error.errors else "Unexpected error"
        raise GraphQLError(message=error_message) from auth_error
