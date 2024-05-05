"""Fetching messages for display in OptHub Client."""

from gql import gql

from opthub_client.graphql.client import get_gql_client


class VersionCLIMessage:
    """Version CLI Message."""

    label: str
    label_color: str
    message: str
    message_color: str

    def __init__(self, label: str, labelColor: str, message: str, messageColor: str):
        self.label = label
        self.label_color = labelColor
        self.message = message
        self.message_color = messageColor


def get_messages(version: str) -> list[VersionCLIMessage]:
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
    if isinstance(data, list) and data:
        messages = [VersionCLIMessage(**item) for item in data]
        return messages
    raise ValueError("No CLI messages found for version")
