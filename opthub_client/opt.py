"""This module contains the OptHub CLI client entrypoint."""

import click

from opthub_client.controllers.create import create
from opthub_client.controllers.download import download
from opthub_client.controllers.help import help
from opthub_client.controllers.login import login
from opthub_client.controllers.logout import logout
from opthub_client.controllers.select import select
from opthub_client.controllers.show import show
from opthub_client.controllers.submit import submit

custom_style = {
    "question": "fg:#ffff00 bold",  # question text style
    "answer": "fg:#f44336 bold",  # answer text style
    "input": "fg:#ffeb3b",  # input field style
    "pointer": "fg:#00bcd4 bold",  # select pointer style
    "highlighted": "fg:#00bcd4 bold",  # highlighted item style
    "selected": "fg:#cddc39 bold",  # selected text style
    "instruction": "",  # instruction text style
    "text": "",  # normal text style
}


@click.group(help="OptHub CLI client.")
@click.version_option()
@click.pass_context
def opt(ctx: click.Context) -> None:  # noqa: ARG001
    """This function is for OptHub CLI client entrypoint."""


opt.add_command(show)
opt.add_command(select)
opt.add_command(submit)
opt.add_command(help)
opt.add_command(login)
opt.add_command(logout)
opt.add_command(download)
opt.add_command(create)
