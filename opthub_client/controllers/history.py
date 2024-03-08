import click
from opthub_client.context.match_selection import MatchSelectionContext
from opthub_client.models.trial import Trial
from prompt_toolkit import PromptSession, HTML
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit.styles import Style
import sys

style = Style.from_dict({
    'n': 'fg:blue bold',  
    'e': 'fg:red bold', 
})

show_size = 5
first = True

def display_trials(trials):
        if trials:
            lines = ""
            for trial in trials:
                lines += "Trial No: " + str(trial.id) + "\n"
                lines += "Solution: " + str(trial.solution.variable) + "\n"
                lines += "Evaluation: " + str(trial.evaluation.objective) + "\n"
                lines += "Score: " + str(trial.score.score) + "\n"
            click.echo(lines.rstrip())
        else:
            click.echo("No more solutions to display.")
            
@click.command()
@click.pass_context
def history(ctx,**kwargs):
    """Check submitted solutions."""
    bindings = KeyBindings()
    match_selection = MatchSelectionContext()
    match_selection.load()
    current_comp = match_selection.competition_id
    current_match = match_selection.match_id

    @bindings.add('n')
    def _(event):
        """Display next batch of solutions."""
        trials = Trial.fetch_list(None,"aa",1,show_size)
        run_in_terminal(lambda: display_trials(trials), render_cli_done=False)
        
    @bindings.add('e')
    @bindings.add('q')
    @bindings.add('c-c')
    def _(event):
        """Exit the application."""
        sys.exit()

    # Initialize prompt session with key bindings.
    session = PromptSession(key_bindings=bindings)
    
    # The initial call to display next batch of solutions.
    # (Directly using the logic inside the _ function above.)
    trials = Trial.fetch_list(None,"aa",1,show_size)
    display_trials(trials)
    
    while True:
        session.prompt(HTML('<n style="class:n">n</n>: more solutions, <e style="class:e">e</e>: exit \n'), key_bindings=bindings,style=style)

    