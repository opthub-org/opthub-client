"""This module contains the methods for context."""

from pathlib import Path


def get_opthub_client_dir() -> Path:
    """Get the opthub client directory."""
    opthub_dir = Path.home() / ".opthub_client"
    opthub_dir.mkdir(exist_ok=True)  # Create the directory if it doesn't exist
    return opthub_dir
