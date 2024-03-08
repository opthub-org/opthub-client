import click
import logging

from opthub_client.controllers.history import history
from opthub_client.controllers.select import select
from opthub_client.controllers.submit import submit
from opthub_client.controllers.help import help
_logger = logging.getLogger(__name__)

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
@click.option(
    "-r",
    "--role",
    envvar="OPTHUB_ROLE",
    type=click.Choice(["anonymous", "user", "admin"], case_sensitive=False),
    default="user",
    help="Role based access control.",
)
@click.option(
    "--verify/--no-verify",
    envvar="OPTHUB_VERIFY",
    default=True,
    help="Verity SSL certificate.",
)
@click.option(
    "-t",
    "--retries",
    envvar="OPTHUB_RETRIES",
    type=click.IntRange(min=0),
    default=0,
    help="Retries for HTTPS connection.",
)
@click.option("-q", "--quiet", count=True, help="Be quieter.")
@click.option("-v", "--verbose", count=True, help="Be more verbose.")

@click.option(
    "-a",
    "--auth-url",
    envvar="OPTHUB_AUTH_URL",
    type=str,
    default="https://opthub.us.auth0.com",
    help="Authentication URL.",
)
@click.option(
    "-i",
    "--auth-client-id",
    envvar="OPTHUB_AUTH_CLIENT_ID",
    type=str,
    default="E3JSaUuGCopA8To7e8SttdOv28l3x3Mf",
    help="Authentication client ID.",
)
@click.option(
    "--access-token",
    envvar="OPTHUB_ACCESS_TOKEN",
    type=str,
    help="OptHub access token.",
)
@click.option(
    "--refresh-token",
    envvar="OPTHUB_REFRESH_TOKEN",
    type=str,
    help="OptHub refresh token.",
)
@click.option("--id-token", envvar="OPTHUB_ID_TOKEN", type=str, help="OptHub ID token.")
@click.version_option()
@click.pass_context
def opt(ctx, **kwargs):
    """The entrypoint of CLI.

    :param ctx: Click context
    :param kwargs: Click options
    """
    verbosity = 10 * (kwargs["quiet"] - kwargs["verbose"])
    log_level = logging.WARNING + verbosity
    logging.basicConfig(level=log_level)
    _logger.info("Log level is set to %d.", log_level)
    _logger.info("opt(%s)", kwargs)
    ctx = kwargs
    
opt.add_command(history)
opt.add_command(select)
opt.add_command(submit)
opt.add_command(help)