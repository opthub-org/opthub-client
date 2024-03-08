# competition class
class Competition:
    def __init__(self,attributes):
        self.name = attributes.get("name")
        self.matches = attributes.get("matches")
        pass
    # TODO: mock => GraphQL fetch
    @staticmethod
    def fetch_participated_list(graphql_client):
        competitions = []
        for i in range(5):
            comp = Competition({"name":"League "+chr(i+65)})
            competitions.append(comp)
        return competitions