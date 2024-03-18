import click
from src.controllers.auth import sign_in
from src.controllers.history import history
from src.controllers.select import select
from src.controllers.submit import submit

@click.group(help="OptHub CLI client.")
@click.pass_context
def help():
    """Show commands usage."""
    pass

help.add_command(history)
help.add_command(select)
help.add_command(submit)
help.add_command(sign_in)
