"""Fetching messages for display in OptHub Client."""

from gql import gql

from opthub_client.graphql.client import get_gql_client


class VersionCLIMessage:
    label: str
    labelColor: str
    message: str
    messageColor: str


def get_messages(version: str) -> VersionCLIMessage | None:
    """Get messages for display in OptHub Client.

    Returns:
        dict[str, str]: The messages.
    """
    client = get_gql_client()
    query = gql("""
    query getCLIVersionStatus($version: String) {
    getCLIVersionStatus(version: $version) {
        label
        labelColor
        message
        messageColor
    }
    }
    """)

    result = client.execute(query, variable_values={"version": version})
    data = result.get("getCLIVersionStatus")
    if data:
        return VersionCLIMessage(**data)
    return None
