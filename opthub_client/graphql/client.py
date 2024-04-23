"""This module contains the GraphQL client getter."""

from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport


def get_gql_client(access_token: str | None) -> Client:
    """Get the GraphQL client.

    Args:
        access_token (str | None): The access token

    Returns:
        Client: The GraphQL client

    """
    url = "https://jciqso7l7rhajfkt5s3dhybpcu.appsync-api.ap-northeast-1.amazonaws.com/graphql"
    api_key = "da2-kge2w7onkfcodd6wx4m437uie4"
    headers = {"x-api-key": api_key} if access_token is None else {"Authorization": f"Bearer {access_token}"}
    transport = AIOHTTPTransport(url=url, headers=headers)
    return Client(transport=transport, fetch_schema_from_transport=True)
