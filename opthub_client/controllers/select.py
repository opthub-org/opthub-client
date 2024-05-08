"""This module contains the functions related to select command."""

import click
from InquirerPy import prompt  # type: ignore[attr-defined]

from opthub_client.context.match_selection import MatchSelectionContext
from opthub_client.models.competition import fetch_participated_competitions
from opthub_client.models.match import fetch_matches_by_competition

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

MOCK_USER_ID = "7f0ffdfb-279e-4cb2-900b-347751e1ad24"
MOCK_USER_NAME = "kumamoto"


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
    match_selection_context = MatchSelectionContext()

    # competitions aliases for choices
    competitions = fetch_participated_competitions(MOCK_USER_ID, MOCK_USER_NAME)
    competition_aliases = [competition["alias"] for competition in competitions]

    # if not set -c commands option
    if competition is None:
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
            competition = result_competition["competition"]
        else:
            click.echo("Input type is not valid.")
            return
    if competition not in competition_aliases:
        click.echo("Competition is not found.")
        return
    selected_competition = next((c for c in competitions if c["alias"] == competition), None)
    if selected_competition is None:
        click.echo("Competition is not found.")
        return
    matches = fetch_matches_by_competition(selected_competition["id"], selected_competition["alias"])
    match_aliases = [match["alias"] for match in matches]

    # if not set -m commands option
    if match is None:
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
            click.echo("Input type is not valid.")
            return
    if match not in match_aliases:
        click.echo("Match is not found.")
        return
    selected_match = next((m for m in matches if m["alias"] == match), None)
    if selected_match is None:
        click.echo("Match is not found.")
        return
    match_selection_context.update(selected_competition, selected_match)

    # show selected competition and match
    click.echo(f"You have selected {competition} - {match}")
