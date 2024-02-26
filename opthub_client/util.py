import click
from prompt_toolkit.validation import Validator, ValidationError
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
import re

def display_trials(trials, show_label=False):
    """Display a batch of solutions, optionally showing a label."""
    if show_label:
        click.echo("solutions:") 
    solutions_str = print_lines(trials)
    click.echo(solutions_str.rstrip())

def print_lines(trials):
    lines = ""
    for trial in trials:
        lines += "Trial No: " + str(trial.solution.trial_no) + "\n"
        lines += "Solution: " + str(trial.solution.var) + "\n"
        lines += "Evaluation: " + str(trial.evaluation.obj) + "\n"
        lines += "Score: " + str(trial.score.score) + "\n"
    return lines


class SolutionValidator(Validator):
    def validate(self, document):
        pattern = r'^\[(\d|\d+\.\d+)+(\s*,\s*(\d|\d+\.\d+)+)*\s*\]$'
        if not re.match(pattern, document.text):
            raise ValidationError(
                message="Invalid format. Please enter in the format [number,number,...,number].",
                cursor_position=len(document.text))


def execute(ctx, document, variable_values=None):
    """Execute a GraphQL document and print results.

    :param ctx: Click context
    :param document: GraphQL document
    :param variable_values: variables
    :return dict: GraphQL response
    """
    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    }
    transport = RequestsHTTPTransport(
        url=ctx.obj["url"],
        use_json=True,
        headers=headers,
    )
    client = Client(
        transport=transport,
        fetch_schema_from_transport=True,
    )
    
    print("Executing the query...")
    results = client.execute(gql(document), variable_values=variable_values)
    print("...Executed.")

    return results

