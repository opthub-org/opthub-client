import click
from src.context.match_selection import MatchSelectionContext
from src.models.trial import fetch_trial_list
from prompt_toolkit import PromptSession, HTML
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit.styles import Style
import sys

style = Style.from_dict({
    'n': 'fg:blue bold',  
    'e': 'fg:red bold', 
})

def display_trials(trials):
        if trials is None:
            click.echo("No more solutions to display.")
        else:
            lines = ""
            for trial in trials:
                lines += "Trial No: " + str(trial["id"]) + "\n"
                lines += "Solution: " + str(trial["solution"]["variable"]) + "\n"
                lines += "Evaluation: " + str(trial["evaluation"]["objective"]) + "\n"
                lines += "Score: " + str(trial["score"]["score"]) + "\n"
            click.echo(lines.rstrip())
            
@click.command()
@click.option(
    "-s",
    "--size",
    type=click.IntRange(1, 50), # show size of trials must be 1-50
    default=10,
    help="Number of trials to display (1-50)."
)
@click.option("-c", "--competition", type=str, help="Competition ID.")
@click.option("-m", "--match", type=str, help="Match ID.")
@click.pass_context
def history(ctx,**kwargs):
    """Check submitted solutions."""
    if(kwargs["match"] and kwargs["competition"]):
        competition = kwargs["competition"]
        match = kwargs["match"]
    elif(kwargs["match"]):
        match_selection = MatchSelectionContext()
        competition = match_selection.competition_id
        match = kwargs["match"]
    else:
        match_selection = MatchSelectionContext()
        competition = match_selection.competition_id
        match = match_selection.match_id
    bindings = KeyBindings()
    # n key is to display next batch of solutions
    @bindings.add('n')
    def _(event):
        """Display next batch of solutions."""
        trials = fetch_trial_list(competition,match,1,kwargs["size"])
        run_in_terminal(lambda: display_trials(trials), render_cli_done=False)
        
    @bindings.add('e') # e for exit
    @bindings.add('q') # q for quit
    @bindings.add('c-c') # Ctrl-C
    def _(event):
        """Exit the application."""
        sys.exit()

    # Initialize prompt session with key bindings.
    session = PromptSession(key_bindings=bindings)
    
    # The initial call to display next batch of solutions.
    # (Directly using the logic inside the _ function above.)
    trials = fetch_trial_list(competition,match,1,kwargs["size"])
    display_trials(trials)
    while True:
        # Prompt the user for more solutions(n key) or exit(e or q or Ctrl+c).
        session.prompt(HTML('<n style="class:n">n</n>: more solutions, <e style="class:e">e</e>: exit \n'), key_bindings=bindings,style=style)

    