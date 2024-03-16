import click
import logging

from opthub_client.controllers.auth import signin
from opthub_client.controllers.history import history
from opthub_client.controllers.select import select
from opthub_client.controllers.submit import submit
from opthub_client.controllers.help import help

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
@click.option(
    "-u",
    "--url",
    envvar="OPTHUB_URL",
    type=str,
    default="http://192.168.1.174:20002",
    help="OptHub URL.",
)
@click.version_option()
@click.pass_context
def opt(ctx, **kwargs):
    """The entrypoint of CLI.

    :param ctx: Click context
    :param kwargs: Click options
    """
    ctx = kwargs
    
opt.add_command(history)
opt.add_command(select)
opt.add_command(submit)
opt.add_command(help)
opt.add_command(signin)