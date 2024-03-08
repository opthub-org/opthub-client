# score class
class Score:
    def __init__(self,attributes) :
        self.score= attributes.get("score")
        self.status = attributes.get("status")
        self.created_at = attributes.get("created_at")
        self.started_at = attributes.get("started_at")
        self.finished_at = attributes.get("finished_at")
        pass
    # TODO: mock => GraphQL fetch
    @staticmethod
    def fetch_list(graphql_client,pk,page,size):
        scores = []
        for i in range(size):
            score = Score({"score":i,"status":"success","created_at":"2024-02-25T12:00:00Z","started_at":"2024-02-25T12:00:00Z","finished_at":"2024-02-25T12:00:00Z"})
            scores.append(score)
        return scores

       
