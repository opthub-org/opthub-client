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
        variable = list(map(float, variable))
        return all(isinstance(value, (int | float)) for value in variable)
