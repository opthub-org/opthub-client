class Match:
    def __init__(self,attributes):
        self.name = attributes.get("name")
        pass
    # TODO: mock => GraphQL fetch
    @staticmethod
    def fetch_participated_list_by_competition_id(graphql_client,competition_id):
        matches = []
        for i in range(3):
            match = Match({"name":"Match "+str(i)})
            matches.append(match)
        return matches