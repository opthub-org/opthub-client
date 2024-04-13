"""This module contains the class related to credentials."""

import shelve
import tempfile
from pathlib import Path


class Credentials:
    """The credentials class."""

    def __init__(self) -> None:
        """Initialize the credentials context with a persistent temporary file."""
        temp_dir = tempfile.gettempdir()
        temp_file_name = "credentials"
        self.file_path = Path(temp_dir) / temp_file_name

    def load(self) -> None:
        """Load the credentials from the shelve file."""
        with shelve.open(str(self.file_path)) as db:
            self.access_token = db.get("access_token")
            self.refresh_token = db.get("refresh_token ")
            db.close()

    def update(self, access_token: str, refresh_token: str) -> None:
        """Update the credentials in the shelve file.

        Args:
            access_token (str): access token
            refresh_token(str): refresh token
        """
        with shelve.open(str(self.file_path)) as db:
            db["access_token"] = access_token
            db["refresh_token"] = refresh_token
            db.sync()

    def is_expired_access_token(self) -> bool:
        """Check if the access token is expired."""
        if self.access_token is None or not isinstance(self.access_token, (str)):
            # TODO none or not string type processing
            return True
        try:
            jwt.decode(self.access_token, verify=False)
        except jwt.ExpiredSignatureError:
            return True
        else:
            return False

    def refresh_token(self) -> None:
        """Refresh the access token."""
        # TODO refresh token
        pass
