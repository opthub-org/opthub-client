"""test for auth_client.py"""

from typing import Any

from gql import gql

from opthub_client.graphql.client import get_gql_client


def test_auth(access_token: str) -> None:
    """Create a solution by AppSync endpoint.

    Args:
        match_id (str): The match ID.
        variable (object): The variable of solution.
    """
    client = get_gql_client(access_token)
    info = gql("""
    query info {
        info {
            name
            version
            stage
            uid
        }
        }
    """)
    # クエリを実行し、レスポンスを取得
    response = client.execute(info)

    # レスポンスの内容を表示
    print(response)
