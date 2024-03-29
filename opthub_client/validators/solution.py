"""This module contains the solution validator."""


class SolutionValidator:
    """The solution validator."""

    @staticmethod
    def check_solution(variable: list[float]) -> bool:
        """Check validate the solution.

        Args:
            variable (list[float]): The variable of solution.

        Returns:
            bool: True if the solution is valid, False otherwise.
        """
        if not isinstance(variable, list):
            return False
        return all(isinstance(value, (int | float)) for value in variable)
