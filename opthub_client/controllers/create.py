"""Create object."""

import click

from opthub_client.controllers.create_api_key import api_key


@click.group()
def create() -> None:
    """Create object."""


create.add_command(api_key)
