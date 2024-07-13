"""Read version from toml file."""

import tomllib
from pathlib import Path

from opthub_client.errors.cache_io_error import CacheIOError, CacheIOErrorMessage


def get_version_from_file() -> str:
    """Read version from pyproject.toml file.

    Returns:
        str: The version of the project as a string.

    Raises:
        VersionNotFoundError: If the version cannot be found or is in an incorrect format.
    """
    path = Path("pyproject.toml")
    with path.open("rb") as file:
        data = tomllib.load(file)
    version = data["tool"]["project"]["version"]
    if not isinstance(version, str):
        raise CacheIOError(CacheIOErrorMessage.VERSION_FILE_READ_FAILED)
    return version
