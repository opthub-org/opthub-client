from prompt_toolkit.validation import Validator, ValidationError
import re

class SolutionValidator(Validator):
    def validate(self, document):
        pattern = r'^(\d|\d+\.\d+)+(\s*,\s*(\d|\d+\.\d+)+)*\s*$'
        if not re.match(pattern, document.text):
            raise ValidationError(
                message="Invalid format. Please enter in the format number,number,...,number",
                cursor_position=len(document.text))
