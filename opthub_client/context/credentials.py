"""This module contains the class related to credentials."""

import shelve
import time
from pathlib import Path
from typing import Any

import boto3
import jwt
import requests
from jwcrypto import jwk  # type: ignore[import]

from opthub_client.context.cipher_suite import CipherSuite
from opthub_client.context.utils import get_opthub_client_dir
from opthub_client.errors.authentication_error import AuthenticationError, AuthenticationErrorMessage

FILE_NAME = "credentials"
CLIENT_ID = "24nvfsrgbuvu75h4o8oj2c2oek"
JWKS_URL = "https://cognito-idp.ap-northeast-1.amazonaws.com/ap-northeast-1_1Y69fktA0/.well-known/jwks.json"


class Credentials:
    """The credentials class. To store and manage the credentials."""

    file_path: Path
    access_token: str | None
    refresh_token: str | None
    expire_at: str | None
    uid: str | None
    username: str | None

    def __init__(self) -> None:
        """Initialize the credentials context with a persistent temporary file."""
        self.file_path = get_opthub_client_dir() / FILE_NAME

    def load(self) -> None:
        """Load the credentials from the shelve file."""
        cipher_suite = CipherSuite()
        with shelve.open(str(self.file_path)) as key_store:
            # decrypt the credentials
            self.access_token = cipher_suite.decrypt(key_store.get("access_token", b""))
            self.refresh_token = cipher_suite.decrypt(key_store.get("refresh_token", b""))
            self.expire_at = cipher_suite.decrypt(key_store.get("expire_at", b""))
            self.uid = cipher_suite.decrypt(key_store.get("uid", b""))
            self.username = cipher_suite.decrypt(key_store.get("username", b""))
            # refresh the access token if it is expired
            if self.is_expired():
                self.refresh_access_token()
            key_store.close()

    def update(self, access_token: str, refresh_token: str) -> None:
        """Update the credentials in the shelve file."""
        cipher_suite = CipherSuite()
        with shelve.open(str(self.file_path)) as key_store:
            # encrypt the credentials
            key_store["access_token"] = cipher_suite.encrypt(access_token)
            key_store["refresh_token"] = cipher_suite.encrypt(refresh_token)
            # decode the access token to get the expire time, user id and user name
            public_key = self.get_jwks_public_key(access_token)
            token = jwt.decode(access_token, public_key, algorithms=["RS256"], options={"verify_signature": True})
            key_store["expire_at"] = cipher_suite.encrypt(str(token.get("exp")))
            key_store["uid"] = cipher_suite.encrypt(token.get("sub"))
            key_store["username"] = cipher_suite.encrypt(token.get("username"))
            key_store.sync()
        self.access_token = access_token
        self.refresh_token = refresh_token

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
        """Refresh the access token using refresh token.

        Returns:
            bool: true if the access token is refreshed successfully, otherwise false.
        """
        try:
            client = boto3.client("cognito-idp", region_name="ap-northeast-1")
            response = client.initiate_auth(
                AuthFlow="REFRESH_TOKEN_AUTH",
                AuthParameters={"REFRESH_TOKEN": self.refresh_token},
                ClientId=CLIENT_ID,
            )
            self.access_token = response["AuthenticationResult"]["AccessToken"]
            if self.access_token is None:
                self.clear_credentials()
                return
            public_key = self.get_jwks_public_key(self.access_token)
            self.expire_at = jwt.decode(
                self.access_token,
                public_key,
                algorithms=["RS256"],
                options={"verify_signature": True},
            )["exp"]
        except:
            self.clear_credentials()

    def cognito_login(self, username: str, password: str) -> None:
        """Login to cognito user pool. And update the credentials.

        Args:
            username (str): username
            password (str): password
        """
        try:
            client = boto3.client("cognito-idp", region_name="ap-northeast-1")
            response = client.initiate_auth(
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={"USERNAME": username, "PASSWORD": password},
                ClientId=CLIENT_ID,
            )
            access_token = response["AuthenticationResult"]["AccessToken"]
            refresh_token = response["AuthenticationResult"]["RefreshToken"]
            self.update(access_token, refresh_token)
        except Exception as e:
            raise AuthenticationError(AuthenticationErrorMessage.LOGIN_FAILED) from e

    def clear_credentials(self) -> None:
        """Clear the credentials in the shelve file."""
        with shelve.open(str(self.file_path)) as key_store:
            key_store.clear()
            key_store.sync()
        self.access_token = None
        self.refresh_token = None
        self.expire_at = None
        self.uid = None
        self.username = None

    def get_jwks_public_key(self, access_token: str) -> Any:  # noqa: ANN401
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
            raise AuthenticationError(AuthenticationErrorMessage.GET_JWKS_PUBLIC_KEY_FAILED) from e
        jwks = response.json()
        headers = jwt.get_unverified_header(access_token)
        kid = headers["kid"]
        for key in jwks["keys"]:
            if key["kid"] == kid:
                jwk_obj = jwk.JWK(**key)
                public_key_pem = jwk_obj.export_to_pem()
                return public_key_pem
        raise AuthenticationError(AuthenticationErrorMessage.GET_JWKS_PUBLIC_KEY_FAILED)
