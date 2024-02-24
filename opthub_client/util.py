import click
from prompt_toolkit.validation import Validator, ValidationError
import re
def show_solutions(solutions):
    solutions_str = print_json_lines(solutions)
    click.echo(solutions_str.rstrip())

def print_json_lines(data, indent=0):
    lines = ""
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                lines += print_json_lines(item, indent + 1)
            else:
                lines +=  " "+str(data) + "\n"
                return lines
    elif isinstance(data, dict):
        for key, value in data.items():
            prefix = "  " * indent
            if isinstance(value, dict) or isinstance(value, list):
                lines += f"{prefix}{key}:" + print_json_lines(value, indent + 1)
            else:
                lines += f"{prefix}{key}: {value}\n"
    return lines

    

class SolutionValidator(Validator):
    def validate(self, document):
        # if len(document.text) > 50:
        #     raise ValidationError(
        #         message='Too long.',
        #         cursor_position=len(document.text))
        pattern = r'^\[\d+(\s*,\d+)*\s*\]$'
        if not re.match(pattern, document.text):
            raise ValidationError(
                message="Invalid format. Please enter in the format [number,number,...,number].",
                cursor_position=len(document.text))

