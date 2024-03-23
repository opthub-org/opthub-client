"""This module contains the class related to match selection context."""

import sys
from pathlib import Path

import click

from opthub_client.models.competition import Competition, fetch_participated_competitions
from opthub_client.models.match import Match, fetch_matches_by_competition_alias


class MatchSelectionContext:
    """The selection context of match."""

    match_id: str | None
    competition_id: str | None
    file_path: str

    def __init__(self) -> None:
        """Initialize the match selection context."""
        self.file_path = ".match_selection"
        self.competition_id = None
        self.match_id = None
        self.load()

    def load(self) -> None:
        """Load the match selection from file."""
        if Path.exists(Path(self.file_path)) is not True:
            # file is not found
            self.competition_id = None
            self.match_id = None
            return
        try:
            with Path.open(Path(self.file_path)) as file:
                content = file.read()
                parts = content.split(",")
                self.competition_id = parts[0]
                self.match_id = parts[1]
        except OSError as e:
            click.echo(
                f"An error occurred while reading the file: {e}. Please select competition and match again",
                file=sys.stderr,
            )
            self.competition_id = None
            self.match_id = None
            return

    def update(self, competition_id: str, match_id: str) -> None:
        """Update the match selection.

        Args:
            competition_id (str): Competition ID
            match_id (str): Match ID
        """
        self.competition_id = competition_id
        self.match_id = match_id
        with Path.open(Path(self.file_path), "w") as file:
            file.write(competition_id + "," + match_id)

def match_select(match: str | None, competition: str | None) ->tuple[Competition,Match]:
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
    match_selection_context.update(selected_competition["alias"], selected_match["alias"])
    return selected_competition,selected_match
