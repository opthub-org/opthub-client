"""This module contains the functions related to matches."""

from typing import TypedDict

from gql import gql

from opthub_client.graphql.client import get_gql_client


class Match(TypedDict):
    """This class represents the match type."""

    id: str
    alias: str


def fetch_matches_by_competition(comp_id: str, comp_alias: str) -> list[Match]:
    """Fetch matches by competition alias.

    Args:
        alias (str): Competition Alias

    Returns:
        list[Match]: Matches related to the competition
    """
    client = get_gql_client()
    query = gql("""
        query getMatchesByCompetition(
        $id: String,
        $alias: String
        ) {
        getMatchesByCompetition(
            id: $id,
            alias: $alias
        ) {
            id
            competition {
            ...CompetitionFragment
            }
            problem {
            ...ProblemFragment
            }
            indicator {
            ...IndicatorFragment
            }
            title
            alias
            successTrialsBudget
            submissionsBudget
            isTutorial
            problemPublicEnvironments {
            ...KeyValueFragment
            }
            indicatorPublicEnvironments {
            ...KeyValueFragment
            }
            problemPrivateEnvironments {
            ...NullableKeyValueFragment
            }
            indicatorPrivateEnvironments {
            ...NullableKeyValueFragment
            }
            openAt
            closeAt
        }
        }""")
    result = client.execute(query, variable_values={"id": comp_id, "alias": comp_alias})
    data = result.get("getMatchesByCompetition")
    if data and isinstance(data, list):
        return [Match(id=match["id"], alias=match["alias"]) for match in data]
    error_message = "Failed to fetch participated matches."
    raise ValueError(error_message)
