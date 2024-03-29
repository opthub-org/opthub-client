"""This module contains the class related to match selection context."""

import shelve
import tempfile
from pathlib import Path

from opthub_client.models.competition import Competition
from opthub_client.models.match import Match


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
