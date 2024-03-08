import click
from InquirerPy import prompt
from opthub_client.context.match_selection import MatchSelectionContext
from opthub_client.models.competition import Competition
from opthub_client.models.match import Match

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
def select(**kwargs):
    """Select a competition and match."""
    match_select = MatchSelectionContext()
    # competitions names for choices
    comp_names = [comp.name for comp in Competition.fetch_participated_list(None)]
    comp_questions = [
    {
        "type": "list",
        "message": "Select a competition:",
        "name": "competition",
        "choices": comp_names,
    }, ]
    # if not set -c commands option
    if kwargs["competition"] not in comp_names:
        comp_result = prompt(questions=comp_questions,style=custom_style)
        comp = comp_result["competition"]    
    match_names = [match.name for match in Match.fetch_participated_list_by_competition_id(None,comp)]
    match_questions = [
    {
        "type": "list",
        "message": "Select a match:",
        "name": "match",
        "choices": match_names,
    }, ]
    # if not set -m commands option 
    if kwargs["match"] not in match_names:
        match_result = prompt(questions=match_questions,style=custom_style)
        match = match_result["match"]
    # show selected competition and match
    click.echo(f"You have selected {comp} - {match}")
    match_select.update(comp,match)
