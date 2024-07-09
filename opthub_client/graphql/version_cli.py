"""Fetching messages for display in OptHub Client."""

from gql import gql
from gql.transport.exceptions import TransportQueryError

from opthub_client.errors.graphql_error import GraphQLError
from opthub_client.errors.query_error import QueryError
from opthub_client.graphql.client import get_gql_client


class VersionCLIMessage:
    """Version CLI Message."""

    label: str
    label_color: str
    message: str
    message_color: str

    def __init__(self, label: str, label_color: str, message: str, message_color: str) -> None:
        """Initialize the VersionCLIMessage class.

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
        result = client.execute(query, variable_values={"version": version})
        data = result.get("getCLIVersionStatus")
        if not data:
            raise QueryError(resource="version status", detail="No data returned.")
        if not isinstance(data, list):
            raise QueryError(resource="version status", detail="Invalid data returned.")
    except TransportQueryError as auth_error:
        error_message = auth_error.errors[0]["message"] if auth_error.errors else "Unexpected error"
        raise GraphQLError(message=error_message) from auth_error
    else:
        messages = [VersionCLIMessage(**item) for item in data]
        return messages
