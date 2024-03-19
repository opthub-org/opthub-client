import click
from context.match_selection import MatchSelectionContext
from InquirerPy import prompt
from models.competition import fetch_participated_competitions
from models.match import fetch_matches_by_competition_alias

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
@click.pass_context
def select(
    ctx: click.Context,
    competition: str | None,
    match: str | None,
) -> None:
    """Select a competition and match."""
    match_selection_context = MatchSelectionContext()
    # competitions names for choices
    competition_aliases = [competition["alias"] for competition in fetch_participated_competitions()]

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
        selected_competition = prompt(questions=competition_questions, style=custom_style)
        competition = selected_competition["competition"]

    if competition not in competition_aliases:
        click.echo("Competition is not found.")
        return

    match_aliases = [match["alias"] for match in fetch_matches_by_competition_alias(competition)]

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
        selected_match = prompt(questions=match_questions, style=custom_style)
        match = selected_match["match"]

    if match not in match_aliases:
        click.echo("Match is not found.")
        return

    # show selected competition and match
    click.echo(f"You have selected {competition} - {match}")
    match_selection_context.update(competition, match)
