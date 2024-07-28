"""Read version from init.py file."""

from pathlib import Path

from opthub_client.errors.cache_io_error import CacheIOError, CacheIOErrorMessage


def get_version_from_init() -> str:
    """Read version from [project]/init.py file.

    Returns:
        str: The version of the project as a string.

    Raises:
        VersionNotFoundError: If the version cannot be found or is in an incorrect format.
    """
    path = Path("opthub_client/__init__.py")
    if not path.is_file():
        raise CacheIOError(CacheIOErrorMessage.VERSION_FILE_READ_FAILED)
    try:
        with path.open("r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("__version__"):
                    version = line.split("=")[1].strip().strip('"')
                    if version:
                        return version
        raise CacheIOError(CacheIOErrorMessage.VERSION_FILE_READ_FAILED)
    except Exception as e:
        raise CacheIOError(CacheIOErrorMessage.VERSION_FILE_READ_FAILED) from e
