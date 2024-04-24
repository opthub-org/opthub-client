"""This module contains the class related to credentials."""

import shelve
import tempfile
import time
from pathlib import Path

import boto3
import jwt

CLIENT_ID = "7et20feq5fv89j4k430f7ren7s"
SECRET_HASH = "nrTpTfTDw72mKzN8AD3q813oAH81HpVNFu9+j9g9bLs="


class Credentials:
    """The credentials class. To store and manage the credentials."""

    file_path: Path
    access_token: str
    refresh_token: str
    expire_at: str
    user_id: str
    user_name: str

    def __init__(self) -> None:
        """Initialize the credentials context with a persistent temporary file."""
        temp_dir = tempfile.gettempdir()
        temp_file_name = "opthub_credentials"
        self.file_path = Path(temp_dir) / temp_file_name

    def load(self) -> None:
        """Load the credentials from the shelve file."""
        with shelve.open(str(self.file_path)) as db:
            self.access_token = db.get("access_token", str)
            self.refresh_token = db.get("refresh_token", str)
            self.expire_at = db.get("expire_at", str)
            self.user_id = db.get("user_id", str)
            self.user_name = db.get("user_name", str)
            # refresh the access token if it is expired
            if self.is_expired():
                self.refresh_access_token()
            db.close()

    def update(
        self,
        access_token: str,
        refresh_token: str,
    ) -> None:
        """Update the credentials in the shelve file.

        Args:
            access_token (str): access token
            refresh_token (str): refresh token
            user_id (str): user id
        """
        with shelve.open(str(self.file_path)) as db:
            db["access_token"] = access_token
            db["refresh_token"] = refresh_token
            # decode the access token to get the expire time, user id and user name
            token = jwt.decode(access_token, options={"verify_signature": False})
            db["expire_at"] = token.get("exp")
            db["user_id"] = token.get("sub")
            db["user_name"] = token.get("username")
            db.sync()

    def is_expired(self) -> bool:
        """Determine if the access token has expired.

        Returns:
            bool: True if the token has expired, otherwise False.
        """
        if self.expire_at is None:
            return True
        current_time = int(time.time())
        expire_at_timestamp = int(self.expire_at)
        return current_time > expire_at_timestamp

    def refresh_access_token(self) -> None:
        """Refresh the access token using refresh token."""
        client = boto3.client("cognito-idp", region_name="ap-northeast-1")
        response = client.initiate_auth(
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={"REFRESH_TOKEN": self.refresh_token, "SECRET_HASH": SECRET_HASH},
            ClientId=CLIENT_ID,
        )
        self.access_token = response["AuthenticationResult"]["AccessToken"]
        self.expire_at = jwt.decode(self.access_token, options={"verify_signature": False})["exp"]
