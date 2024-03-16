import json
import click
from InquirerPy.validator import PathValidator
from InquirerPy import prompt
from pathlib import Path
from src.context.match_selection import MatchSelectionContext
from src.models.solution import create_solution
from src.validators.solution_validator import SolutionValidator

@click.command()
@click.option(
    "-c",
    "--competition",
    type=str,
    help="Competition ID",
)
@click.option(
    "-m",
    "--match",
    type=str,
    help="Match ID",
)
@click.option(
    "-f",
    "--file",
    is_flag=True,
    help="Flag to indicate file submission.",
)
@click.pass_context
def submit(ctx,**kwargs):
    """Submit a solution."""
    if(kwargs["match"] and kwargs["competition"]):
        selected_match = kwargs["match"]
        selected_competition = kwargs["competition"]
    elif(kwargs["match"]):
        match_selection = MatchSelectionContext()
        selected_competition = match_selection.competition_id
        selected_match = kwargs["match"]
    else:
        match_selection = MatchSelectionContext()
        selected_competition = match_selection.competition_id
        selected_match = match_selection.match_id
    if(selected_competition is None or selected_match is None):
        click.echo("Please select a competition and match first.")
        return
    if kwargs["file"]: # file submission
        questions = [
        {
            "name": "file",
            "type": "filepath",
            "message": "Submit the solution file (must be a JSON file):",
            "default": str(Path('~/')),
            "validate": PathValidator(is_file=True, message="Input is not a file"),
            "only_files": True,
        },
        ]
        result = prompt(questions)
        variable = Path(result).read_text()
    else: # text submission
        questions = [
                {
                    "name": "solution",
                    "type": "input",
                    "message": "Write the solution:",
                    "validate": SolutionValidator()
                },
                ]
        result = prompt(questions)
        variable = [float(x) for x in result["solution"].split(",")]
        variable = json.dumps(variable)
    click.echo(f"Submitting {result} for Competition: {selected_competition}, Match: {selected_match}...")
    create_solution(selected_competition,selected_match,variable) 
    click.echo("...Submitted.")