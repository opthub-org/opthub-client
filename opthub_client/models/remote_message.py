"""Fetching messages for display in OptHub Client."""

from gql import gql

from opthub_client.errors.graphql_error import GraphQLError
from opthub_client.errors.query_error import QueryError
from opthub_client.graphql.client import execute_graphql


class RemoteMessage:
    """Remote Message."""

    label: str
    label_color: str
    message: str
    message_color: str

    def __init__(self, label: str, label_color: str, message: str, message_color: str) -> None:
        """Initialize the RemoteMessage class.

        Args:
            label (str): label
            label_color (str): color of the label
            message (str): message
            message_color (str): color of the message
        """
        self.label = label
        self.label_color = label_color
        self.message = message
        self.message_color = message_color


def get_version_status_messages(version: str) -> list[RemoteMessage]:
    """Get messages for display in OptHub Client.

    Returns:
        dict[str, str]: The messages.
    """
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
    try:
        result = execute_graphql(query, variables={"version": version})
    except GraphQLError as e:
        raise QueryError(resource="version status", detail=str(e.message)) from e
    data = result.get("getCLIVersionStatus")
    if not data:
        raise QueryError(resource="version status", detail="No data returned.")
    if not isinstance(data, list):
        raise QueryError(resource="version status", detail="Invalid data returned.")
    return [
        RemoteMessage(
            label=item["label"],
            label_color=item["labelColor"],
            message=item["message"],
            message_color=item["messageColor"],
        )
        for item in data
    ]
