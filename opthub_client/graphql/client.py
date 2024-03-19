"""This module contains the GraphQL client getter."""

from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport

url = "MOCK_URL"
api_key = "MOCK_API_KEY"
headers = {"x-api-key": api_key}
transport = AIOHTTPTransport(url=url, headers=headers)
client = Client(transport=transport, fetch_schema_from_transport=True)


def get_gql_client() -> Client:
    """Get the GraphQL client.

    Returns:
        Client: The GraphQL client
    """
    url = "MOCK_URL"
    api_key = "MOCK_API_KEY"
    headers = {"x-api-key": api_key}
    transport = AIOHTTPTransport(url=url, headers=headers)
    return Client(transport=transport, fetch_schema_from_transport=True)
