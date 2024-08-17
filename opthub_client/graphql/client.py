"""This module contains the GraphQL client getter."""

from typing import Any

from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError
from graphql import DocumentNode

from opthub_client.context.credentials import Credentials
from opthub_client.errors.graphql_error import GraphQLError

URL = "https://tf5tepcpn5bori46x5cyxh3ehe.appsync-api.ap-northeast-1.amazonaws.com/graphql"


def get_gql_client() -> Client:
    """Get the GraphQL client.

    Returns:
        Client: The GraphQL client

    Raises:
        AuthenticationError: If authentication fails
    """
    credentials = Credentials()
    credentials.load()
    headers = {"Authorization": f"Bearer {credentials.access_token}"}
    transport = AIOHTTPTransport(url=URL, headers=headers)
    return Client(transport=transport, fetch_schema_from_transport=True)


def execute_graphql(request: DocumentNode, variables: dict[str, Any] | None = None) -> dict[str, Any]:
    """Execute a graphql request.

    Args:
        request (DocumentNode): graphql client request
        variables (_type_, optional): query variables. Defaults to None.

    Raises:
        GraphQLError: graphql error

    Returns:
        dict[str, Any]: result
    """
    client = get_gql_client()
    try:
        return client.execute(request, variable_values=variables)
    except TransportQueryError as auth_error:
        error_message = auth_error.errors[0]["message"] if auth_error.errors else "Unexpected error"
        raise GraphQLError(message=error_message) from auth_error


async def execute_graphql_async(request: DocumentNode, variables: dict[str, Any] | None = None) -> dict[str, Any]:
    """Execute a graphql request.

    Args:
        request (DocumentNode): graphql client request
        variables (_type_, optional): query variables. Defaults to None.

    Raises:
        GraphQLError: graphql error

    Returns:
        dict[str, Any]: result
    """
    client = get_gql_client()
    try:
        return await client.execute_async(request, variable_values=variables)
    except TransportQueryError as auth_error:
        error_message = auth_error.errors[0]["message"] if auth_error.errors else "Unexpected error"
        raise GraphQLError(message=error_message) from auth_error
