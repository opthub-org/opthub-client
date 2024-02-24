import click
from opthub_client.history import history
from opthub_client.select_prompt import select_prompt
from opthub_client.submit import submit

@click.group(help="OptHub CLI client.")
@click.pass_context
def help():
    """Show commands usage."""
    pass

help.add_command(history)
help.add_command(select_prompt)
help.add_command(submit)

if __name__ == '__main__':
    help()