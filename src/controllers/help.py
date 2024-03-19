import click

from controllers.auth import auth
from controllers.history import history
from controllers.select import select
from controllers.submit import submit


@click.group(help="OptHub CLI client.")
@click.pass_context
def help(ctx: click.Context) -> None:  # noqa: A001, ARG001
    """Show commands usage."""


help.add_command(history)
help.add_command(select)
help.add_command(submit)
help.add_command(auth)
