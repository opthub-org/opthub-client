import click
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit import HTML
from prompt_toolkit.styles import Style
from opthub_client.util import show_solutions
import sys 

# style def
style = Style.from_dict({
    'n': 'fg:blue bold',  
    'e': 'fg:red bold', 
})
current_competition = "League A"
current_match = "Match1"
solution_size = 5
    
solution = {
    'League A': {
        'Match1': [
            {
                'value': [12, 34], 
                'evaluation': 1
             }, 
            {
                'value': [8, 12], 
                'evaluation': 2
            }, 
            {
                'value': [12, 18], 
                'evaluation': 3
            }, 
            {
                'value': [16, 24], 
                'evaluation': 4
            }, 
            {
                'value': [22, 33],
                'evaluation': 5
            },
            {
                'value': [14, 21],
                'evaluation': 6
            }, 
            {
                'value': [24, 21],
                'evaluation': 7
            },
            {
                'value': [34, 11],
                'evaluation': 8
            },
            {
                'value': [34, 1],
                'evaluation': 9
            },
            {
                'value': [44, 21],
                'evaluation': 10
            },
            {
                'value': [54, 21],
                'evaluation': 11
            },
            ],
        'Match2': [
            {
            'value': [4, 6], 
            'evaluation': 52
            },{
            'value': [10, 15], 
            'evaluation': 55
            },  {
            'value': [18, 27], 
            'evaluation': 59
            } ],
        'Match3': [
            {
            'value': [6, 9], 
            'evaluation': 53
            }, {
            'value': [20, 30],
            'evaluation': 60
            },  
            ],
        },
    'League B': {
        'Match1': [{
            'value': [3, 4],
            'evaluation': 56
            },  {
            'value': [21, 31],
            'evaluation': 65
            },],
        'Match2': [{
            'value': [5, 7],
            'evaluation': 57
            },  {
            'value': [19, 28],
            'evaluation': 64
            }, {
            'value': [11, 16],
            'evaluation': 60
            },{
            'value': [13, 19],
            'evaluation': 61
            },{
            'value': [15, 22],
            'evaluation': 62
            },],
        'Match3': [{
            'value': [7, 10],
            'evaluation': 58
            }, {
            'value': [9, 13],
            'evaluation': 59
            },{
            'value': [17, 25],
            'evaluation': 63
            },]

        }
    }

def get_solution_batches(match_solutions, batch_size):
    """Yield consecutive batches of solutions."""
    for i in range(0, len(match_solutions), batch_size):
        yield match_solutions[i:i + batch_size]

def display_solutions(batch, show_label=False):
    """Display a batch of solutions, optionally showing a label."""
    if show_label:
        click.echo("solutions:") 
    show_solutions(batch)

@click.command()
@click.option(
    "-c",
    "--competition",
    type=str,
    default=current_competition,
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
        run_in_terminal(display_next_batch, render_cli_done=False)

    @bindings.add('e')
    @bindings.add('q')
    @bindings.add('c-c')
    def _(event):
        """Exit the application."""
        sys.exit()

    def display_next_batch():
        nonlocal current_index
        current_index += 1
        batch = next(solution_batches, None)
        if batch:
            display_solutions(batch, show_label=(current_index == 0))
        else:
            click.echo("No more solutions to display.")
            current_index -= 1  # Stay at current index if no more batches

    # Initialize prompt session with key bindings.
    session = PromptSession(key_bindings=bindings)

    # Get the initial batch of solutions and display it.
    if solution.get(competition) == None:
        click.echo(f"no solution in {competition}")
        return
    if solution.get(competition).get(match) == None:
        click.echo(f"no solution in {match}")
        return 
    match_solutions = solution.get(competition).get(match)
    solution_batches = get_solution_batches(match_solutions, solution_size)
    current_index = -1  # Start with first batch

    display_next_batch()
    
    while True:
        session.prompt(HTML('<n style="class:n">n</n>: more solutions, <e style="class:e">e</e>: exit '), key_bindings=bindings,style=style)
   
if __name__ == '__main__':
    history()
