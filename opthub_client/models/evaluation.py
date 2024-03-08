# evaluation class
class Evaluation:
    def __init__(self,attributes) :
        self.objective = attributes.get("objective")
        self.constraint = attributes.get("constraint")
        self.status = attributes.get("status")
        self.created_at = attributes.get("created_at")
        self.started_at = attributes.get("started_at")
        self.finished_at = attributes.get("finished_at")
        pass
    # TODO: mock => GraphQL fetch
    @staticmethod
    def fetch_list(graphql_client,pk,page,size):
        evals = []
        for i in range(size):
            eval = Evaluation({"objective":i,"constraint":i**2,"status":"success","created_at":"2024-02-25T12:00:00Z","started_at":"2024-02-25T12:00:00Z","finished_at":"2024-02-25T12:00:00Z"})
            evals.append(eval)
        return evals

       
