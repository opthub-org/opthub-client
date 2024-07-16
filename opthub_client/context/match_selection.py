"""This module contains the class related to match selection context."""

import shelve

from opthub_client.context.utils import get_opthub_client_dir
from opthub_client.errors.cache_io_error import CacheIOError, CacheIOErrorMessage
from opthub_client.errors.user_input_error import UserInputError, UserInputErrorMessage
from opthub_client.models.competition import Competition, fetch_participating_competitions
from opthub_client.models.match import Match, fetch_matches_by_competition

FILE_NAME = "match_selection"


class MatchSelectionContext:
    """The selection context of match."""

    def __init__(self) -> None:
        """Initialize the match selection context with a persistent temporary file."""
        self.file_path = get_opthub_client_dir() / FILE_NAME
        self.load()

    def load(self) -> None:
        """Load the match selection from the shelve file."""
        with shelve.open(str(self.file_path)) as key_store:  # noqa: S301 opthub-client#95
            self.competition_id = key_store.get("competition_id")
            self.match_id = key_store.get("match_id")
            self.match_alias = key_store.get("match_alias")
            self.competition_alias = key_store.get("competition_alias")
            key_store.close()

    def update(self, competition: Competition, match: Match) -> None:
        """Update the match selection in the shelve file.

        Args:
            competition (Competition): Competition instance
            match (Match): Match instance
        """
        with shelve.open(str(self.file_path)) as db:  # noqa: S301 opthub-client#95
            db["competition_id"] = competition["id"]
            db["match_id"] = match["id"]
            db["match_alias"] = match["alias"]
            db["competition_alias"] = competition["alias"]
            db.sync()

    def get_selection(self, match: str | None, competition: str | None) -> tuple[Competition, Match]:
        """Select a competition and match based on the provided aliases.

        This method allows you to select a competition and a match by their aliases.
        If no aliases are provided, it will use default values from `MatchSelectionContext`.
        If the competition or match cannot be found, it raises an appropriate error or exits the program.

        Args:
            match (str | None): The alias of the match to select.
                                If None, it uses the default value from `MatchSelectionContext`.
            competition (str | None): The alias of the competition to select.
                                      If None, it uses the default value from `MatchSelectionContext`.

        Returns:
            tuple[Competition, Match]: A tuple containing the selected competition and match objects.

        """
        match_selection_context = MatchSelectionContext()
        if match is None:
            match = match_selection_context.match_alias
        if competition is None:
            competition = match_selection_context.competition_alias
        if competition is None or match is None:
            raise CacheIOError(CacheIOErrorMessage.MATCH_SELECTION_FILE_READ_FAILED)
        # competitions aliases for choices
        competitions = fetch_participating_competitions()
        selected_competition = next((c for c in competitions if c["alias"] == competition), None)
        if selected_competition is None:
            raise UserInputError(UserInputErrorMessage.COMPETITION_ERROR)
        matches = fetch_matches_by_competition(selected_competition["id"], selected_competition["alias"])
        selected_match = next((m for m in matches if m["alias"] == match), None)
        if selected_competition is None:
            raise UserInputError(UserInputErrorMessage.COMPETITION_ERROR)
        if selected_match is None:
            raise UserInputError(UserInputErrorMessage.MATCH_ERROR)
        return selected_competition, selected_match

    def get_match(self, match: str | None, competition: str | None) -> Match:
        """Select a match based on the provided aliases.

        This method allows you to select a match by its alias within a specified competition.
        If no aliases are provided, it will use default values from `MatchSelectionContext`.
        If the competition or match cannot be found, it raises an appropriate error or exits the program.

        Args:
            match (str | None): The alias of the match to select.
                                If None, it uses the default value from `MatchSelectionContext`.
            competition (str | None): The alias of the competition to select.
                                      If None, it uses the default value from `MatchSelectionContext`.

        Returns:
            Match: The selected match object.
        """
        match_selection_context = MatchSelectionContext()
        if match is None:
            match = match_selection_context.match_alias
        if competition is None:
            competition = match_selection_context.competition_alias
        if competition is None or match is None:
            raise CacheIOError(CacheIOErrorMessage.MATCH_NOT_SELECTED)
        competitions = fetch_participating_competitions()
        selected_competition = next((c for c in competitions if c["alias"] == competition), None)
        if selected_competition is None:
            raise UserInputError(UserInputErrorMessage.COMPETITION_ERROR)
        matches = fetch_matches_by_competition(selected_competition["id"], selected_competition["alias"])
        selected_match = next((m for m in matches if m["alias"] == match), None)
        if selected_competition is None:
            raise UserInputError(UserInputErrorMessage.COMPETITION_ERROR)
        if selected_match is None:
            raise UserInputError(UserInputErrorMessage.MATCH_ERROR)
        return selected_match
