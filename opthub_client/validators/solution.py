"""This module contains the solution validator."""

import json


class SolutionValidator:
    """The solution validator."""

    @staticmethod
    def check_solution(raw_solution: str) -> bool:
        """Check validate the solution.

        Args:
            raw_solution (str): The raw data of solution.

        Returns:
            bool: True if the solution is valid, False otherwise.
        """
        try:
            variable = json.loads(raw_solution)
            # Check if variable is a scalar number (int or float)
            if isinstance(variable, (int | float)):
                return True
            # Check if variable is a list of numbers
            if isinstance(variable, list):
                # Each element of variable is float or int
                variable = list(map(float, variable))
                return all(isinstance(value, (float)) for value in variable)
        except (ValueError, json.JSONDecodeError):
            return False
        else:
            # If variable is not a scalar number or a list of numbers return false
            return False
