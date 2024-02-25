import click
from InquirerPy import prompt
from opthub_client.model import fetch_competitions
import datetime
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
# fetch competitions 
all_comps = fetch_competitions(datetime.datetime.now())

# competitions names for choices
comp_names = [comp.name for comp in all_comps]

@click.command()
@click.option("-c", "--comp", type=str, help="Competition ID.")
@click.option("-m", "--match", type=str, help="Match ID.")
def select(comp, match):
    """Select a competition and match."""
    comp_questions = [
    {
        "type": "list",
        "message": "Select a competition:",
        "name": "competition",
        "choices": comp_names,
    }, ]
    # if not set -c commands option
    if comp not in comp_names:
        comp_result = prompt(questions=comp_questions,style=custom_style)
        comp = comp_result["competition"]    
    selected_comp = next((competition for competition in all_comps if competition.get_name() == comp), None)
    match_names = [match.get_name() for match in selected_comp.get_all_matches()]
    match_questions = [
    {
        "type": "list",
        "message": "Select a match:",
        "name": "match",
        "choices": match_names,
    }, ]
    # if not set -m commands option 
    if match not in match_names:
        match_result = prompt(questions=match_questions,style=custom_style)
        match = match_result["match"]
    # show selected competition and match
    click.echo(f"You have selected {comp} - {match}")

if __name__ == '__main__':
    select()
