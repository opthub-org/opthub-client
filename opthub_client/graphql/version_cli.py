"""Fetching messages for display in OptHub Client."""

from gql import gql

from opthub_client.errors.graphql_error import GraphQLError
from opthub_client.errors.query_error import QueryError
from opthub_client.graphql.client import execute_query, get_gql_client


class VersionCLIMessage:
    """Version CLI Message."""

    label: str
    label_color: str
    message: str
    message_color: str

    def __init__(self, label: str, labelColor: str, message: str, messageColor: str) -> None:
        """Initialize the VersionCLIMessage class.

        Args:
            label (str): label
            labelColor (str): color of the label
            message (str): message
            messageColor (str): color of the message
        """
        self.label = label
        self.label_color = labelColor
        self.message = message
        self.message_color = messageColor


def get_version_status_messages(version: str) -> list[VersionCLIMessage]:
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
    try:
        result = execute_query(client, query, variables={"version": version})
        data = result.get("getCLIVersionStatus")
        if not data:
            raise QueryError(resource="version status", detail="No data returned.")
        if not isinstance(data, list):
            raise QueryError(resource="version status", detail="Invalid data returned.")
        return [VersionCLIMessage(**item) for item in data]
    except GraphQLError as e:
        raise QueryError(resource="version status", detail=str(e.message)) from e
