"""Fetching messages for display in OptHub Client."""

from gql import gql

from opthub_client.graphql.client import get_gql_client


class VersionCLIMessage:
<<<<<<< HEAD
    """Version CLI Message."""

    label: str
    label_color: str
    message: str
    message_color: str

    def __init__(self, label: str, label_color: str, message: str, message_color: str):
        self.label = label
        self.labelColor = label_color
        self.message = message
        self.messageColor = message_color


def get_messages(version: str) -> VersionCLIMessage:
=======
    label: str
    labelColor: str
    message: str
    messageColor: str


def get_messages(version: str) -> VersionCLIMessage | None:
>>>>>>> cd87f36 (:sparkles: add version graphql)
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
<<<<<<< HEAD
    if isinstance(data, list) and data:
        return VersionCLIMessage(**data[0])
    raise ValueError("No CLI messages found for version")
=======
    if data:
        return VersionCLIMessage(**data)
    return None
>>>>>>> cd87f36 (:sparkles: add version graphql)
