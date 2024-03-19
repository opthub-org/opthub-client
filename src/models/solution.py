from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

# TODO: 別ファイルに分離
url = "MOCK_URL"
api_key = "MOCK_API_KEY"
headers = {"x-api-key": api_key}
transport = AIOHTTPTransport(url=url, headers=headers)
client = Client(transport=transport, fetch_schema_from_transport=True)

Variable = list[float] | float


def create_solution(match_id: str, variable: Variable) -> None:
    """Create a solution by AppSync endpoint.

    Args:
        match_id (str): The match ID.
        variable (object): The variable of solution.
    """
    mutation = gql("""
    mutation CreateSolution($input: CreateSolutionInput!) {
        createSolution(input: $input) {
            matchId
            trialNo
        }
    }
    """)
    variables = {
        "input": {
            "matchId": match_id,
            "variable": variable,
        },
    }
    client.execute(mutation, variable_values=variables)
