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
        variable = json.loads(raw_solution)
        # variable is not list
        if isinstance(variable, list):
            return True
        variable = [variable]
        try:
            # each element of variable is float or int
            variable = list(map(float, variable))
        except ValueError:
            # if any element of variable is not float or int
            return False
        return all(isinstance(value, (int | float)) for value in variable)
