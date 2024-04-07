"""This module contains the class related to match selection context."""

import shelve
import tempfile
from pathlib import Path

import click

from opthub_client.models.competition import Competition, fetch_participated_competitions
from opthub_client.models.match import Match, fetch_matches_by_competition_alias


class MatchSelectionContext:
    """The selection context of match."""

    def __init__(self) -> None:
        """Initialize the match selection context with a persistent temporary file."""
        temp_dir = tempfile.gettempdir()
        temp_file_name = "match_selection"
        self.file_path = Path(temp_dir) / temp_file_name
        self.db = shelve.open(str(self.file_path))
        self.load()

    def load(self) -> None:
        """Load the match selection from the shelve file."""
        self.competition_id = self.db.get("competition_id")
        self.match_id = self.db.get("match_id")
        self.match_alias = self.db.get("match_alias")
        self.competition_alias = self.db.get("competition_alias")

    def update(self, competition: Competition, match: Match) -> None:
        """Update the match selection in the shelve file.

        Args:
            competition (Competition): Competition instance
            match (Match): Match instance
        """
        self.db["competition_id"] = competition["id"]
        self.db["match_id"] = match["id"]
        self.db["match_alias"] = match["alias"]
        self.db["competition_alias"] = competition["alias"]
        self.db.sync()

    def get_selection(self, match: str | None, competition: str | None) -> tuple[Competition, Match]:
        """Select a match."""
        match_selection_context = MatchSelectionContext()
        if match is None:
            match = match_selection_context.match_id
        if competition is None:
            competition = match_selection_context.competition_id
        if competition is None or match is None:
            msg = "Please select a competition and match first."
            raise AssertionError(msg)
        competitions = fetch_participated_competitions()
        selected_competition = next((c for c in competitions if c["alias"] == competition), None)
        matches = fetch_matches_by_competition_alias(competition)
        selected_match = next((m for m in matches if m["alias"] == match), None)
        if selected_competition is None:
            msg = "Competition is not found."
            raise AssertionError(msg)
        if selected_match is None:
            msg = "Match is not found."
            raise AssertionError(msg)
        return selected_competition, selected_match
