"""This module contains the functions related to select command."""

import click
from InquirerPy import prompt  # type: ignore[attr-defined]

from opthub_client.context.match_selection import MatchSelectionContext
from opthub_client.controllers.utils import check_current_version_status
from opthub_client.errors.authentication_error import AuthenticationError
from opthub_client.errors.cache_io_error import CacheIOError
from opthub_client.errors.fetch_error import FetchError
from opthub_client.errors.query_error import QueryError
from opthub_client.errors.user_input_error import UserInputError, UserInputErrorMessage
from opthub_client.models.competition import Competition, fetch_participating_competitions
from opthub_client.models.match import Match, fetch_matches_by_competition

custom_style = {
    "question": "fg:#ffff00 bold",  # question text style
    "answer": "fg:#f44336 bold",  # answer text style
    "input": "fg:#ffeb3b",  # input field style
    "pointer": "fg:#00bcd4 bold",  # select pointer style
    "highlighted": "fg:#00bcd4 bold",  # highlighted item style
    "selected": "fg:#cddc39 bold",  # selected text style
    "instruction": "",  # instruction text style
    "text": "",  # normal text style
}


@click.command()
@click.option("-c", "--competition", type=str, help="Competition ID.")
@click.option("-m", "--match", type=str, help="Match ID.")
def select(
    competition: str | None,
    match: str | None,
) -> None:
    """Select a competition and match.

    Args:
        competition (str | None): option for competition(-c or --competition)
        match (str | None): option for match(-m or --match)
    """
    try:
        check_current_version_status()
        match_selection_context = MatchSelectionContext()
        # competitions aliases for choices
        competitions = fetch_participating_competitions()
        if len(competitions) == 0:
            click.echo("No competitions found that you are participating in.")
            return
        selected_competition = select_competition(competitions, competition)
        matches = fetch_matches_by_competition(selected_competition["id"], selected_competition["alias"])
        selected_match = select_match(matches, match)
        match_selection_context.update(selected_competition, selected_match)
        # show selected competition and match
        click.echo(f"You have selected {selected_competition['alias']}/{selected_match['alias']}")
    except (AuthenticationError, FetchError, QueryError, CacheIOError, UserInputError) as error:
        error.handler()
    except Exception:
        click.echo("Unexpected error occurred. Please try again later.")


def select_competition(competitions: list[Competition], competition_option: str | None) -> Competition:
    """Select a competition.

    Args:
        competitions (list[Competition]): fetch participating competitions
        competition_option (str | None): option for competition(-c or --competition)

    Raises:
        UserInputError: competition error

    Returns:
        Competition: competition
    """
    competition_aliases = [competition["alias"] for competition in competitions]
    # if not set -c commands option
    if competition_option is None:
        competition_questions = [
            {
                "type": "list",
                "message": "Select a competition:",
                "name": "competition",
                "choices": competition_aliases,
            },
        ]
        result_competition = prompt(questions=competition_questions, style=custom_style)
        if isinstance(result_competition["competition"], str):
            competition_option = result_competition["competition"]
        else:
            raise UserInputError(UserInputErrorMessage.COMPETITION_ERROR)
    if competition_option not in competition_aliases:
        raise UserInputError(UserInputErrorMessage.COMPETITION_ERROR)
    selected_competition = next((c for c in competitions if c["alias"] == competition_option), None)
    if selected_competition is None:
        raise UserInputError(UserInputErrorMessage.COMPETITION_ERROR)
    return selected_competition


def select_match(matches: list[Match], match_option: str | None) -> Match:
    """Select a match.

    Args:
        matches (list[Match]): fetch matches
        match_option (str | None): option for match(-m or --match)

    Raises:
        UserInputError: match error

    Returns:
        Match: Match
    """
    match_aliases = [match["alias"] for match in matches]
    # if not set -m commands option
    if match_option is None:
        match_questions = [
            {
                "type": "list",
                "message": "Select a match:",
                "name": "match",
                "choices": match_aliases,
            },
        ]
        result_match = prompt(questions=match_questions, style=custom_style)
        if isinstance(result_match["match"], str):
            match = result_match["match"]
        else:
            raise UserInputError(UserInputErrorMessage.MATCH_ERROR)
    if match not in match_aliases:
        raise UserInputError(UserInputErrorMessage.MATCH_ERROR)
    selected_match = next((m for m in matches if m["alias"] == match), None)
    if selected_match is None:
        raise UserInputError(UserInputErrorMessage.MATCH_ERROR)
    return selected_match
