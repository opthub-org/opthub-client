import click
from InquirerPy import prompt
from opthub_client.context.match_selection import MatchSelectionContext
from opthub_client.models.competition import fetch_participated_competition_list
from opthub_client.models.match import fetch_participated_match_list_by_competition_id

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
def select(ctx,**kwargs):
    """Select a competition and match."""
    match_selection_context = MatchSelectionContext()
    # competitions names for choices
    competition_names = [competition["name"] for competition in fetch_participated_competition_list()]
    competition_questions = [
    {
        "type": "list",
        "message": "Select a competition:",
        "name": "competition",
        "choices": competition_names,
    }, ]
    # if not set -c commands option
    if kwargs["competition"] not in competition_names:
        selected_competition = prompt(questions=competition_questions,style=custom_style)
        competition = selected_competition["competition"]    
    match_names = [match["name"] for match in fetch_participated_match_list_by_competition_id(competition)]
    match_questions = [
    {
        "type": "list",
        "message": "Select a match:",
        "name": "match",
        "choices": match_names,
    }]
    # if not set -m commands option 
    if kwargs["match"] not in match_names:
        selected_match = prompt(questions=match_questions,style=custom_style)
        match = selected_match["match"]
    # show selected competition and match
    click.echo(f"You have selected {competition} - {match}")
    match_selection_context.update(competition,match)
