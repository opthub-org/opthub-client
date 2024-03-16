from src.lib import graphql
def fetch_solution_list(competition_id, match_id, page, size):
    # mock data
    solutions = [{
        'variable': 3,
        'created_at': '2021-01-01',
    }]
    return solutions

def create_solution(competition_id, match_id, variable):
    # mock data
    new_solution = {
        'variable': variable,
        'created_at': '2021-01-01',
    }
    return new_solution
