"""This module contains the functions related to competitions."""

from typing import TypedDict


class Competition(TypedDict):
    """This class represents the competition type."""

    id: str
    alias: str


def fetch_participated_competitions() -> list[Competition]:
    """Fetch competitions and matches that the user is participating in.

    Returns:
        list[Competition]: Competitions and matches that the user is participating in
    """
    return [
        {
            "id": "2a322f8b-f6d7-342c-5ab3-32320f953d51",
            "alias": "competition1",
        },
        {
            "id": "2a322f8b-f6d7-342c-5ab3-32320f953d51",
            "alias": "competition2",
        },
    ]
