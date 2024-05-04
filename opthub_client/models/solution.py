"""Solution model."""

from gql import gql

from opthub_client.graphql.client import get_gql_client

Variable = list[float] | float


def create_solution(match_id: str, variable: Variable) -> None:
    """Create a solution by AppSync endpoint.

    Args:
        match_id (str): The match ID.
        variable (object): The variable of solution.
    """
    client = get_gql_client()
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
    client.execute(mutation, variables)
