import click
from InquirerPy import prompt

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

all_competitions = ['League A', 'League B', 'League C']
all_matches = ['Match 1', 'Match 2', 'Match 3']

@click.command()
@click.option("-c", "--competition", type=click.Choice(all_competitions), help="Competition ID.")
@click.option("-m", "--match", type=click.Choice(all_matches), help="Match ID.")
def select_prompt(competition, match):
    """Select a competition and match."""
    competition_questions = [
    {
        "type": "list",
        "message": "Select a competition:",
        "name": "competition",
        "choices": ["League A", 
                    "League B",
                    "League C"],
    }, ]
    if not competition:
        competition_result = prompt(questions=competition_questions,style=custom_style)
        competition = competition_result["competition"]    
    match_questions = [
    {
        "type": "list",
        "message": "Select a match:",
        "name": "match",
        "choices": ["Match 1", 
                    "Match 2",
                    "Match 3"],
    }, ]
    if not match:
        match_result = prompt(questions=match_questions,style=custom_style)
        match = match_result["match"]
    # 選択結果の表示
    click.echo(f"You have selected {competition} - {match}")

if __name__ == '__main__':
    select_prompt()
