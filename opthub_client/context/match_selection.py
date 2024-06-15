"""This module contains the class related to match selection context."""

import shelve
import sys
from pathlib import Path

import click

from opthub_client.models.competition import Competition, fetch_participating_competitions
from opthub_client.models.match import Match, fetch_matches_by_competition


class MatchSelectionContext:
    """The selection context of match."""

    def __init__(self) -> None:
        """Initialize the match selection context with a persistent temporary file."""
        home_dir = Path.home()
        opthub_client_dir = home_dir / ".opthub_client"
        opthub_client_dir.mkdir(exist_ok=True)  # Create the directory if it doesn't exist
        self.file_path = opthub_client_dir / "match_selection"
        self.load()

    def load(self) -> None:
        """Load the match selection from the shelve file."""
        with shelve.open(str(self.file_path)) as db:
            self.competition_id = db.get("competition_id")
            self.match_id = db.get("match_id")
            self.match_alias = db.get("match_alias")
            self.competition_alias = db.get("competition_alias")
            db.close()

    def update(self, competition: Competition, match: Match) -> None:
        """Update the match selection in the shelve file.

        Args:
            competition (Competition): Competition instance
            match (Match): Match instance
        """
        with shelve.open(str(self.file_path)) as db:
            db["competition_id"] = competition["id"]
            db["match_id"] = match["id"]
            db["match_alias"] = match["alias"]
            db["competition_alias"] = competition["alias"]
            db.sync()

    def get_selection(self, match: str | None, competition: str | None) -> tuple[Competition, Match]:
        """Select a match."""
        match_selection_context = MatchSelectionContext()
        if match is None:
            match = match_selection_context.match_alias
        if competition is None:
            competition = match_selection_context.competition_alias
        if competition is None or match is None:
            msg = "Please select a competition and match first."
            raise AssertionError(msg)
        competitions = fetch_participating_competitions()
        selected_competition = next((c for c in competitions if c["alias"] == competition), None)
        if selected_competition is None:
            click.echo("Competition is not found.")
            sys.exit(1)
        matches = fetch_matches_by_competition(selected_competition["id"], selected_competition["alias"])
        selected_match = next((m for m in matches if m["alias"] == match), None)
        if selected_competition is None:
            msg = "Competition is not found."
            raise AssertionError(msg)
        if selected_match is None:
            msg = "Match is not found."
            raise AssertionError(msg)
        return selected_competition, selected_match

    def get_selection_match(self, match: str | None, competition: str | None) -> Match:
        """Select a match."""
        match_selection_context = MatchSelectionContext()
        if match is None:
            match = match_selection_context.match_alias
        if competition is None:
            competition = match_selection_context.competition_alias
        if competition is None or match is None:
            msg = "Please select a competition and match first."
            raise AssertionError(msg)
        competitions = fetch_participating_competitions()
        selected_competition = next((c for c in competitions if c["alias"] == competition), None)
        if selected_competition is None:
            click.echo("Competition is not found.")
            sys.exit(1)
        matches = fetch_matches_by_competition(selected_competition["id"], selected_competition["alias"])
        selected_match = next((m for m in matches if m["alias"] == match), None)
        if selected_competition is None:
            msg = "Competition is not found."
            raise AssertionError(msg)
        if selected_match is None:
            msg = "Match is not found."
            raise AssertionError(msg)
        return selected_match
