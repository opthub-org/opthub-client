"""Read version from toml file."""

import tomllib


class VersionNotFoundError(Exception):
    """Exception raised when the version cannot be found or is in an incorrect format."""


def get_version() -> str:
    """Read version from pyproject.toml file.

    Returns:
        str: The version of the project as a string.

    Raises:
        VersionNotFoundError: If the version cannot be found or is in an incorrect format.
    """
    try:
        with open("pyproject.toml", "rb") as file:
            data = tomllib.load(file)
        version = data["tool"]["poetry"]["version"]
        if isinstance(version, str):
            return version
        else:
            raise VersionNotFoundError("Version is not a string.")
    except (KeyError, FileNotFoundError, PermissionError, tomllib.TOMLDecodeError) as e:
        raise VersionNotFoundError(f"Error reading version: {e}")
