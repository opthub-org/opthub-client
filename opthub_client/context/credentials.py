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
        self.db = shelve.open(str(self.file_path))
        self.load()

    def load(self) -> None:
        """Load the credentials from the shelve file."""
        self.username = self.db.get("user_name")
        self.password = self.db.get("password")

    def update(self, username: str, password: str) -> None:
        """Update the credentials in the shelve file.

        Args:
            username (str): _description_
            password (str): _description_
        """
        self.db["user_name"] = username
        self.db["password"] = password
        self.db.sync()
