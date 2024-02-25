import click
from prompt_toolkit.validation import Validator, ValidationError
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

