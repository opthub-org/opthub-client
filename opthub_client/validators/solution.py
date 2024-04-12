"""This module contains the solution validator."""

from typing import Any


class SolutionValidator:
    """The solution validator."""

    @staticmethod
    def check_solution(variable: Any) -> bool:
        """Check validate the solution.

        Args:
            variable (Any): The variable of solution.

        Returns:
            bool: True if the solution is valid, False otherwise.
        """
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
