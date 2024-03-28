"""This module contains the class related to match selection context."""

import sys
from pathlib import Path

import click

from opthub_client.models.competition import Competition
from opthub_client.models.match import Match


class MatchSelectionContext:
    """The selection context of match."""

    match_id: str | None
    competition_id: str | None
    match_alias: str | None
    competition_alias: str | None
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
            self.competition_alias = None
            self.match_alias = None
            return
        try:
            with Path.open(Path(self.file_path)) as file:
                content = file.read()
                parts = content.split(",")
                self.competition_id = parts[0].split(":")[0]
                self.competition_alias = parts[0].split(":")[1]
                self.match_id = parts[1].split(":")[0]
                self.match_alias = parts[1].split(":")[1]
        except OSError as e:
            click.echo(
                f"An error occurred while reading the file: {e}. Please select competition and match again",
                file=sys.stderr,
            )
            self.competition_id = None
            self.competition_alias = None
            self.match_id = None
            self.match_alias = None
            return

    def update(self, competition: Competition, match: Match) -> None:
        """Update the match selection.

        Args:
            competition (Competition): Competition instance
            match (Match): Match instance
        """
        self.competition_id = competition["id"]
        self.competition_alias = competition["alias"]
        self.match_id = match["id"]
        self.match_alias = match["alias"]
        with Path.open(Path(self.file_path), "w") as file:
            file.write(
                self.competition_id + ": " + self.competition_alias + "," + self.match_id + ": " + self.match_alias,
            )
