def fetch_evaluation_list(competition_id, match_id, page, size):
    # mock data
    evaluations = [{
        'objective': 3,
        'constraint': 4,
        'status': 'finished',
        'created_at': '2021-01-01',
        'started_at': "2021-01-01",
        'finished_at': "2021-01-01",
    }]
    return evaluations
