import click
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit import HTML
from prompt_toolkit.styles import Style
from opthub_client.util import display_trials
from opthub_client.model import fetch_trials
import sys 

# style def
style = Style.from_dict({
    'n': 'fg:blue bold',  
    'e': 'fg:red bold', 
})

show_size = 5
current_comp = "League A"
current_match = "Match 1"
first = True
    
def display_next_batch(competition,match):
    global first 
    trials = fetch_trials(show_size)
    if not any(competition in trial.solution.comp_id for trial in trials):
        click.echo(f"no solution in {competition}")
        sys.exit()
    if not any(match in trial.solution.match_id for trial in trials):
        click.echo(f"no solution in {match}")
        sys.exit()
    if trials:
        display_trials(trials, show_label=first )
    else:
        click.echo("No more solutions to display.")
    first = False
   
@click.command()
@click.option(
    "-c",
    "--competition",
    type=str,
    default=current_comp,
    help="Competition ID. default current competition",
)
@click.option(
    "-m",
    "--match",
    type=str,
    default=current_match,
    help="Match ID. default current match",
)

def history(competition, match):
    """Check submitted solutions."""
    bindings = KeyBindings()
    
    @bindings.add('n')
    def _(event):
        """Display next batch of solutions."""
        run_in_terminal(lambda: display_next_batch(competition, match), render_cli_done=False)

    @bindings.add('e')
    @bindings.add('q')
    @bindings.add('c-c')
    def _(event):
        """Exit the application."""
        sys.exit()

    # Initialize prompt session with key bindings.
    session = PromptSession(key_bindings=bindings)
    
    display_next_batch(competition,match)
    
    while True:
        session.prompt(HTML('<n style="class:n">n</n>: more solutions, <e style="class:e">e</e>: exit '), key_bindings=bindings,style=style)
   
if __name__ == '__main__':
    history()
