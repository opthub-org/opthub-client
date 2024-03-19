import re

from prompt_toolkit.document import Document
from prompt_toolkit.validation import ValidationError, Validator


class SolutionValidator(Validator):
    """Validator for the solution input."""

    def validate(self, document: Document) -> None:
        """Validate the solution input."""
        pattern = r"^(\d|\d+\.\d+)+(\s*,\s*(\d|\d+\.\d+)+)*\s*$"
        if not re.match(pattern, document.text):
            raise ValidationError(
                message="Invalid format. Please enter in the format number,number,...,number",
                cursor_position=len(document.text),
            )
