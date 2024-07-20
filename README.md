[日本語版](https://github.com/opthub-org/opthub-client/blob/main/README_ja.md) 👈

# OptHub Client

![Skills](https://skillicons.dev/icons?i=py,graphql,vscode,github)

The Opthub Client is a Python package that provides the following features:

- Submitting solutions to OptHub competitions
- Checking the history and status of solutions submitted to OptHub competitions

This section explains how to install the OptHub Client and provides a tutorial. For more detailed instructions, please refer to the [OptHub Client User Guide](https://opthub.notion.site/OptHub-Client-User-Guide-ece08c9977ec4733b7cbeb2d5bafb797?pvs=4).

## Installation
Make sure you have Python 3.10 or higher installed and that you have set up pip as your package manager. Then, run the following command to install opthub-client from PyPI.

```bash
$ pip install opthub-client
```

## Tutorial

In this tutorial, we will explain how to submit solutions for the competitions you are participating in and how to review the history of your submissions.

To submit solutions, you need to create an account and join a competition beforehand.

👉 [How to Create an Account and Join a Competition](https://opthub.notion.site/Tutorial-23febfdfbb7c41d0893a6681f3e7ae20?pvs=4)

### Login

Execute `opt login` and enter your username and password.

```bash
$ opt login
Username: [username] # Your username
Password: [password]   # Your password
Hello [username]. Successfully logged in.
```

⚠ You need to create an account and verify your email address beforehand.

### Select a Competition and Match

Execute `opt select` and select a competition and match.

```bash
$ opt select
? Select a competition: [competition_id] # Use ↑↓ keys to select a competition
? Select a match: [match_id] # Use ↑↓ keys to select a match
You have selected [competition_id]/[match_id]
```

⚠ You need to join at least one competition beforehand.

### Submit a Solution

Execute `opt submit` and enter a solution according to the competition's input/output requirements.

```bash
$ opt submit
? Write the solution: [your_solution] # Enter your solution
Submitting to [competition_id]/[match_id]... # Submitting
...Submitted # Submission complete
```

👉 [How to Submit a Solution from a File](https://opthub.notion.site/submit-Submit-a-solution-2192134bad9b40c39670b567dd6d8f3f?pvs=4)

### Check Submitted Solutions

Execute `opt show trials` to display the solutions you have submitted. Press `n` to display the next 20 solutions, or press `e` to exit the check.

```bash
$ opt show trials # Displays 20 solutions in descending order by default
Trial No: 30, status: success, Score: 0.0001
Trial No: 29, status: scoring
Trial No: 28, status: evaluating
・・・
n: next solutions, e: exit
# Press n to display the next 20 solutions, e to exit the check
```

### Download Submitted Solutions

Execute `opt download` to download the solutions by specifying the range of trial numbers.

```bash
$ opt download -s 10 -e 30 # Download trial numbers 10 to 30
Downloading trials  [####################################]  100%
Trials have been written to trials_match1.json
```

👉 [Format of the Output JSON File](https://opthub.notion.site/download-Download-the-solutions-c77b44f02df24609a8f04490d6036e77?pvs=4)

## For Contributors

Follow these steps to set up the environment:

1. Clone this repository.
2. Set up Poetry.
3. Run `poetry install`.
4. Download the recommended VSCode Extensions.
5. Disable the following VS Code Extensions for this workspace to avoid conflicts with other packages:
    - ms-python.pylint
    - ms-python.black-formatter
    - ms-python.flake8
    - ms-python.isort

Once you have completed the above setup, you can use the `opt` command in the project's root directory.

## Contact <a id="Contact"></a>

If you have any questions or concerns, please feel free to contact us (Email: dev@opthub.ai).

<img src="https://opthub.ai/assets/images/logo.svg" width="200">

