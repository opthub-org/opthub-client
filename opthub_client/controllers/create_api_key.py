"""Create api key."""

import click

from opthub_client.models.api_key import ApiKey, create_api_key


@click.command(name="api_key")
@click.option("-f", "--force", is_flag=True, help="Force to create key")
def api_key(
    force: bool,
) -> None:
    """Create api key.

    Args:
        force (bool): Force to create key
    """
    if force:
        is_proceed = click.confirm("The issued API_KEY will become invalid. Are you sure you want to proceed?")
        if not is_proceed:
            return
    api_key = create_api_key(force)
    show_message(api_key)


def show_message(api_key: ApiKey) -> None:
    """Show message.

    Args:
        api_key (ApiKey): api key
    """
    click.echo(click.style("The API key will only be displayed once.", fg="red", bold=True))
    click.echo(f"API_KEY: {api_key['value']}")
    click.echo(f"Expires at: {api_key['expires_at']}")
    click.echo("Please store the API key in a safe place. Using the API key allows you to submit and verify solutions.")
