"""Read version from init.py file."""

from opthub_client.__init__ import __version__


def get_version_from_init() -> str:
    """Read version from [project]/init.py file.

    Returns:
        str: The version of the project as a string.

    Raises:
        VersionNotFoundError: If the version cannot be found or is in an incorrect format.
    """
    version = __version__
    return version
