"""Solution model."""

from gql import gql

from opthub_client.graphql.client import get_gql_client


def create_solution(match_id: str, variable: str) -> None:
    """Create a solution by AppSync endpoint.

    Args:
        match_id (str): The match ID.
        variable (object): The variable of solution.
    """
    client = get_gql_client()
    mutation = gql("""
    mutation createSolution(
        $matchId: String!,
        $variable: AWSJSON!) {
        createSolution(
            matchId: $matchId,
            variable: $variable
        ) {
            matchId
            participantType
            participantId
            trialNo
        }
    }
    """)
    solution_input = {
        "matchId": match_id,
        "variable": variable,
    }
    client.execute(mutation, solution_input)
