import click
from opthub_client.controllers.history import history
from opthub_client.controllers.select import select
from opthub_client.controllers.submit import submit

@click.group(help="OptHub CLI client.")
@click.pass_context
def help():
    """Show commands usage."""
    pass

help.add_command(history)
help.add_command(select)
help.add_command(submit)
