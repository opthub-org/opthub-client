import click
from InquirerPy.validator import PathValidator
from InquirerPy import prompt
from pathlib import Path
from opthub_client.context.match_selection import MatchSelectionContext
from opthub_client.lib.util import SolutionValidator
from opthub_client.models.solution import Solution

@click.command()
# @click.option(
#     "-c",
#     "--competition",
#     type=str,
#     help="Competition ID. default current competition",
# )
# @click.option(
#     "-m",
#     "--match",
#     type=str,
#     help="Match ID. default current match",
# )
@click.option(
    "-f",
    "--file",
    is_flag=True,
    help="Flag to indicate file submission.",
)
def submit(**kwargs):
    """Submit a solution."""
    match_selection = MatchSelectionContext()
    match_selection.load()
    current_comp = match_selection.competition_id
    current_match = match_selection.match_id
    # TODO: write error handoling for current_comp and current_match not found
    if kwargs["file"]:
        submit_file(current_comp, current_match)
    else:
        questions = [
                {
                    "name": "solution",
                    "type": "input",
                    "message": "Write the solution:",
                    "validate": SolutionValidator()
                },
                ]
        answers = prompt(questions)
        click.echo(f"Submitting {answers} for Competition: {current_comp}, Match: {current_match}...")
        Solution.create_solution(None,current_comp,current_match) 
        click.echo("...Submitted.")
        
def submit_file(current_comp,current_match):
    questions = [
    {
        "type": "filepath",
        "message": "Submit the solution file (must be a JSON file):",
        "name": "location",
        "default": str(Path('~/')),
        "validate": PathValidator(is_file=True, message="Input is not a file"),
        "only_files": True,
    },
    ]
    result = prompt(questions)
    file_path = Path(result['location']).expanduser()
    click.echo(f"Submitting {result} for Competition: {current_comp}, Match: {current_match}...")
    Solution.create_solution(None,current_comp,current_match) 
    click.echo("...Submitted.")
    