# trial class
from opthub_client.models.evaluation import Evaluation
from opthub_client.models.score import Score
from opthub_client.models.solution import Solution
from enum import Enum, auto

class Status(Enum):
    EVALUATING = auto()
    CALCULATING_SCORE = auto()
    COMPLETED = auto()

class Trial:
    def __init__(self,attributes):
        self.id = attributes.get("id")
        self.solution = attributes.get("solution")
        self.evaluation = attributes.get("evaluation")
        self.score = attributes.get("score")
        self.status = attributes.get("status")
        pass
    # TODO : mock => GraphQL fetch
    @staticmethod
    def fetch_list(graphql_client,pk,page,size):
        trials = []
        sols = Solution.fetch_list(graphql_client,pk,page,size)
        evals = Evaluation.fetch_list(graphql_client,pk,page,size)
        scores = Score.fetch_list(graphql_client,pk,page,size)
        if(len(sols) != len(evals) or len(sols) != len(scores)):
            raise ValueError("invalid size solution, evaluation, score")
        for i in range(size):
            # calcs of score and evaluation is finished
            if(scores[i].score is not None and evals[i].objective is not None):
                status = Status.COMPLETED
            # calcs of score is not finished
            elif scores[i].score is not None:
                status = Status.CALCULATING_SCORE
            # calcs of evaluation is not finished
            else :
                status = Status.EVALUATING
            trial = Trial({"solution":sols[i],"evaluation":evals[i],"score":scores[i],"status":status})
            trials.append(trial)
        return trials