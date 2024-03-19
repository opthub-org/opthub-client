"""This module contains the functions related to matches."""

from typing import TypedDict


class Match(TypedDict):
    """This class represents the match type."""

    id: str
    alias: str


def fetch_matches_by_competition_alias(alias: str) -> list[Match]:
    """Fetch matches by competition alias.

    Args:
        alias (str): Competition Alias

    Returns:
        list[Match]: Matches related to the competition
    """
    return [
        {"id": "2a322f8b-f6d7-342c-5ab3-32320f953d51", "alias": "match1"},
        {"id": "2a322f8b-f6d7-342c-5ab3-32320f953d51", "alias": "match2"},
    ]
