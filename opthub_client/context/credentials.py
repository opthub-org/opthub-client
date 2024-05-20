"""This module contains the class related to credentials."""

import shelve
import time
from pathlib import Path
from typing import Any

import boto3
import jwt
import requests
from cryptography.fernet import Fernet
from jwcrypto import jwk

CLIENT_ID = "24nvfsrgbuvu75h4o8oj2c2oek"
JWKS_URL = "https://cognito-idp.ap-northeast-1.amazonaws.com/ap-northeast-1_1Y69fktA0/.well-known/jwks.json"
KEY_FILE = Path.home() / ".opthub_client" / "encryption_key"
ERROR_MESSAGE_FAIL_TO_GET_PUBLIC_KEY = "Failed to get public key."
ERROR_MESSAGE_FAIL_TO_REFRESH_TOKEN = "Failed to refresh authentication token. Please re-login."
ERROR_MESSAGE_FAIL_TO_GET_JWKS = "Failed to retrieve JWKS"
OPTHUB_CLIENT_DIR = Path.home() / ".opthub_client"


class Credentials:
    """The credentials class. To store and manage the credentials."""

    file_path: Path
    access_token: str
    refresh_token: str
    expire_at: str
    uid: str
    username: str

    def __init__(self) -> None:
        """Initialize the credentials context with a persistent temporary file."""
        OPTHUB_CLIENT_DIR.mkdir(exist_ok=True)  # Create the directory if it doesn't exist
        self.file_path = OPTHUB_CLIENT_DIR / "opthub_credentials"

    def load_or_generate_key(self) -> bytes:
        """Load the encryption key from the shelve file, or generate a new one if it doesn't exist.

        Returns:
            bytes: encryption key
        """
        with shelve.open(str(self.file_path)) as db:
            key = db.get("encryption_key")
            if key is None:
                key = Fernet.generate_key()
                db["encryption_key"] = key
                db.sync()
            return key

    def get_cipher_suite(self) -> Fernet:
        """Get the Fernet cipher suite using the encryption key.

        Returns:
            Fernet: Fernet cipher suite
        """
        encryption_key = self.load_or_generate_key()
        return Fernet(encryption_key)

    def load(self) -> None:
        """Load the credentials from the shelve file."""
        cipher_suite = self.get_cipher_suite()
        with shelve.open(str(self.file_path)) as db:
            # decrypt the credentials
            self.access_token = cipher_suite.decrypt(db.get("access_token", b"")).decode()
            self.refresh_token = cipher_suite.decrypt(db.get("refresh_token", b"")).decode()
            self.expire_at = cipher_suite.decrypt(db.get("expire_at", b"")).decode()
            self.uid = cipher_suite.decrypt(db.get("uid", b"")).decode()
            self.username = cipher_suite.decrypt(db.get("username", b"")).decode()
            # refresh the access token if it is expired
            if self.is_expired() and not self.refresh_access_token():
                self.clear_credentials()
                raise Exception(ERROR_MESSAGE_FAIL_TO_REFRESH_TOKEN)
            db.close()

    def update(self) -> None:
        """Update the credentials in the shelve file."""
        cipher_suite = self.get_cipher_suite()
        with shelve.open(str(self.file_path)) as db:
            # encrypt the credentials
            db["access_token"] = cipher_suite.encrypt(self.access_token.encode())
            db["refresh_token"] = cipher_suite.encrypt(self.refresh_token.encode())
            # decode the access token to get the expire time, user id and user name
            public_key = self.get_jwks_public_key(self.access_token)
            token = jwt.decode(self.access_token, public_key, algorithms=["RS256"], options={"verify_signature": True})
            db["expire_at"] = cipher_suite.encrypt(str(token.get("exp")).encode())
            db["uid"] = cipher_suite.encrypt(token.get("sub").encode())
            db["username"] = cipher_suite.encrypt(token.get("username").encode())
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

    def refresh_access_token(self) -> bool:
        """Refresh the access token using refresh token.

        Returns:
            bool: true if the access token is refreshed successfully, otherwise false.
        """
        client = boto3.client("cognito-idp", region_name="ap-northeast-1")
        try:
            response = client.initiate_auth(
                AuthFlow="REFRESH_TOKEN_AUTH",
                AuthParameters={"REFRESH_TOKEN": self.refresh_token},
                ClientId=CLIENT_ID,
            )
        except Exception:
            return False
        else:
            self.access_token = response["AuthenticationResult"]["AccessToken"]
            public_key = self.get_jwks_public_key(self.access_token)
            self.expire_at = jwt.decode(
                self.access_token,
                public_key,
                algorithms=["RS256"],
                options={"verify_signature": True},
            )["exp"]
        return True

    def cognito_login(self, username: str, password: str) -> None:
        """Login to cognito user pool. And update the credentials.

        Args:
            username (str): username
            password (str): password
        """
        client = boto3.client("cognito-idp", region_name="ap-northeast-1")
        response = client.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": username, "PASSWORD": password},
            ClientId=CLIENT_ID,
        )
        self.access_token = response["AuthenticationResult"]["AccessToken"]
        self.refresh_token = response["AuthenticationResult"]["RefreshToken"]
        self.update()

    def clear_credentials(self) -> None:
        """Clear the credentials in the shelve file."""
        with shelve.open(str(self.file_path)) as db:
            db.clear()
            db.sync()
        self.access_token = ""
        self.refresh_token = ""
        self.expire_at = ""
        self.uid = ""
        self.username = ""

    def get_jwks_public_key(self, access_token: str) -> Any:
        """Get the public key from the JWKS URL.

        Args:
            access_token (str): access token

        Raises:
            ValueError: fail to get JWKS
            ValueError: fail to get public key

        Returns:
            Any: public key
        """
        try:
            response = requests.get(JWKS_URL, timeout=10)  # set timeout 10 seconds
            response.raise_for_status()
        except requests.RequestException as e:
            raise ValueError(ERROR_MESSAGE_FAIL_TO_GET_JWKS) from e
        jwks = response.json()
        headers = jwt.get_unverified_header(access_token)
        kid = headers["kid"]
        for key in jwks["keys"]:
            if key["kid"] == kid:
                jwk_obj = jwk.JWK(**key)
                public_key_pem = jwk_obj.export_to_pem()
                return public_key_pem
        raise ValueError(ERROR_MESSAGE_FAIL_TO_GET_PUBLIC_KEY)
