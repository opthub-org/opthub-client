"""This module contains the class related to match selection context."""

import sys
from pathlib import Path

import click


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
