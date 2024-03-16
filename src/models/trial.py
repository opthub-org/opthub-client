from src.models.evaluation import fetch_evaluation_list
from src.models.score import fetch_score_list
from src.models.solution import fetch_solution_list

def fetch_trial_list(competition_id, match_id, page, size):
    solutions = fetch_solution_list(competition_id, match_id, page, size)
    evaluations = fetch_evaluation_list(competition_id, match_id, page, size)
    scores = fetch_score_list(competition_id, match_id, page, size)

    trials = [{
        "id": i,  
        "solution": solutions[i],
        "evaluation": evaluations[i],
        "score": scores[i],
    } for i in range(len(solutions))]
    return trials
