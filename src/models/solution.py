import json
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

url = "MOCK_URL"
api_key = "MOCK_API_KEY"
headers = {'x-api-key': api_key}
transport = AIOHTTPTransport(url=url, headers=headers)
client = Client(transport=transport, fetch_schema_from_transport=True)

def fetch_solution_list(competition_id, match_id, page, size):
    # mock data
    solutions = [{
        'variable': 3,
        'created_at': '2021-01-01',
    }]
    return solutions

def create_solution(competition_id, match_id, variable):
    participant_id = "User#kuma"
    mutation = gql("""
    mutation CreateSolution($input: CreateSolutionInput!) {
        createSolution(input: $input) {
            matchId
            participantId
            trialNo
        }
    }
    """)
    variables = {
        "input": {
            "matchId": match_id,
            "participantId": participant_id,
            "variable": variable,
        }
    }
    result = client.execute(mutation, variable_values=variables)
    return result