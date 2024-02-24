import click
import logging
import json
import time
from InquirerPy.validator import PathValidator
from InquirerPy import prompt
from pathlib import Path
from opthub_client.util import SolutionValidator

_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@click.command()
@click.option(
    "-c",
    "--competition",
    type=str,
    default="current League A",
    help="Competition ID. default current competition",
)
@click.option(
    "-m",
    "--match",
    type=str,
    default="current Match 1",
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
def submit_file(competition, match):
    _logger.debug("submit(%s)", {'competition': competition, 'match': match})
    questions = [
    {
        "type": "filepath",
        "message": "Submit the solution file (must be a JSON file):",
        "name": "location",
        "default": str(Path('/tmp')),
        "validate": PathValidator(is_file=True, message="Input is not a file"),
        "only_files": True,
    },
    ]

    result = prompt(questions)
    file_path = Path(result['location']).expanduser()
    click.echo(f"Submitting {result} for Competition: {competition}, Match: {match}...")
    if file_path.suffix == ".json":
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                click.echo(click.style(f"Contents of the JSON file: {json.dumps(data, indent=2)}",fg="black",bg="white"))
        except Exception as e:
            click.echo(click.style(f"Failed to read JSON file: {e}",bg="red"))
    else:
        click.echo(click.style("The submitted file is not a JSON file.",bg="red"))
        return
    
    time.sleep(1)
    click.echo("...Submitted.")
    
if __name__ == '__main__':
    submit()
