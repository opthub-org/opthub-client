# solution class
class Solution:
    def __init__(self,attributes) :
        self.variable = attributes.get("variable")
        self.created_at = attributes.get("created_at")
        pass
    # TODO: mock => GraphQL fetch
    @staticmethod
    def fetch_list(graphql_client,pk,page,size):
        sols = []
        for i in range(size):
            sol = Solution({"variable":i,"created_at":"2024-02-25T12:00:00Z"})
            sols.append(sol)
        return sols
    @staticmethod
    def create_solution(graphql_client,comp,match):
        sol = Solution({"variable":0,"created_at":"2024-02-27T12:00:00Z"})
        return sol

       
