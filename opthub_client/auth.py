import click
import logging
import time

_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@click.command()
@click.option(
    "-m",
    "--match",
    type=str,
    required=True,
    help="Match ID.",
)
@click.option(
    "-c",
    "--competition",
    type=str,
    required=True,
    help="Competition ID.",
)

def sing_in(**kwargs):
    """Submit a solution."""
    _logger.debug("submit(%s)", kwargs)
    _logger.info("Submitting a solution...")
    time.sleep(1)
    _logger.info("...Submitted.")

if __name__ == '__main__':
    sing_in()