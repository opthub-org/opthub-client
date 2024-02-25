import click
from InquirerPy.validator import PathValidator
from InquirerPy import prompt
from pathlib import Path
from opthub_client.util import SolutionValidator
from opthub_client.model import create_sol

current_comp = "League A"
current_match = "Match 1"

@click.command()
@click.option(
    "-c",
    "--competition",
    type=str,
    default=current_comp,
    help="Competition ID. default current competition",
)
@click.option(
    "-m",
    "--match",
    type=str,
    default=current_match,
    help="Match ID. default current match",
)
@click.option(
    "-f",
    "--file",
    is_flag=True,
    help="Flag to indicate file submission.",
)

def submit(competition, match, file):
    """Submit a solution."""
    if file:
        submit_file(competition, match)
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
        click.echo(answers)
        create_sol()
        click.echo("...Submitted.")
def submit_file(competition, match):
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
    click.echo(f"Submitting {result} for Competition: {competition}, Match: {match}...")
    create_sol(file_path)
    click.echo("...Submitted.")
    
if __name__ == '__main__':
    submit()
