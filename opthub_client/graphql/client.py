"""This module contains the GraphQL client getter."""

from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport

from opthub_client.context.credentials import Credentials


def get_gql_client() -> Client:
    """Get the GraphQL client.

    Returns:
        Client: The GraphQL client

    """
    url = "https://jciqso7l7rhajfkt5s3dhybpcu.appsync-api.ap-northeast-1.amazonaws.com/graphql"
    credentials = Credentials()
    credentials.load()
    if credentials.access_token is None:
        raise Exception("Please login first.")
    headers = {"Authorization": f"Bearer {credentials.access_token}"}
    transport = AIOHTTPTransport(url=url, headers=headers)
    return Client(transport=transport, fetch_schema_from_transport=True)
