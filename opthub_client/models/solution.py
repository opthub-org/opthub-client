"""Solution model."""

from gql import gql
from graphql import GraphQLError

from opthub_client.errors.mutation_error import Method, MutationError
from opthub_client.graphql.client import execute_mutation, get_gql_client


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
    try:
        execute_mutation(client, mutation, solution_input)
    except GraphQLError as e:
        raise MutationError(method=Method.CREATE, resource="solution", detail="Failed to submit solutions") from e
