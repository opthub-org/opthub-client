"""This module contains the functions related to auth command."""

import boto3
import click

from opthub_client.context.credentials import Credentials

CLIENT_ID = "7et20feq5fv89j4k430f7ren7s"
SECRET_HASH = "nrTpTfTDw72mKzN8AD3q813oAH81HpVNFu9+j9g9bLs="


@click.command()
@click.option("--username", "-u", "user_name", required=True, prompt=True)
@click.option("--password", "-p", "password", prompt=True, hide_input=True)
@click.pass_context
def auth(ctx: click.Context, user_name: str, password: str) -> None:
    """Sign in."""
    client = boto3.client("cognito-idp", region_name="ap-northeast-1")
    response = client.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": user_name, "PASSWORD": password, "SECRET_HASH": SECRET_HASH},
        ClientId=CLIENT_ID,
    )
    access_token = response["AuthenticationResult"]["AccessToken"]
    refresh_token = response["AuthenticationResult"]["RefreshToken"]
    credentials = Credentials()
    credentials.update(access_token, refresh_token)
