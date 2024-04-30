"""This module contains the functions related to auth command."""

import boto3
import click

from opthub_client.context.credentials import Credentials


@click.command()
@click.option("--username", "-u", "username", required=True, prompt=True)
@click.option("--password", "-p", "password", prompt=True, hide_input=True)
@click.pass_context
def auth(ctx: click.Context, username: str, password: str) -> None:
    """Sign in."""
    credentials = Credentials()
    try:
        credentials.cognito_login(username, password)
    except Exception:
        click.echo("Authentication failed. Please verify that your username and password are correct.")
        return
