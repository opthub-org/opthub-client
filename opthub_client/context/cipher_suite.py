"""Cipher Suite Class for encrypting and decrypting data."""

import shelve
from pathlib import Path

from cryptography.fernet import Fernet

KEY_FILE_PATH = Path.home() / ".opthub_client" / "encryption_key"


class CipherSuite:
    """Cipher suite class for encrypt."""

    def get(self) -> Fernet:
        """Get the Fernet cipher suite using the encryption key.

        Returns:
            Fernet: Fernet cipher suite
        """
        encryption_key = self.load_or_generate_key()
        return Fernet(encryption_key)

    def load_or_generate_key(self) -> bytes:
        """Load the encryption key from the shelve file, or generate a new one if it doesn't exist.

        Returns:
            bytes: encryption key
        """
        with shelve.open(str(KEY_FILE_PATH)) as key_store:
            key = key_store.get("encryption_key")
            if key is None:
                key = Fernet.generate_key()
                key_store["encryption_key"] = key
                key_store.sync()
            return key

    def encrypt(self, data: str) -> bytes:
        """Encrypt the data.

        Args:
            data (str): data to encrypt

        Returns:
            bytes: encrypted data
        """
        cipher_suite = self.get()
        return cipher_suite.encrypt(data.encode())

    def decrypt(self, data: bytes) -> str:
        """Decrypt the data.

        Args:
            data (bytes): data to decrypt

        Returns:
            str: decrypted data
        """
        cipher_suite = self.get()
        return cipher_suite.decrypt(data).decode()
