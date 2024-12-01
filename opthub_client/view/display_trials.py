"""This module contains the functions that display the trials to the user."""

from datetime import UTC, datetime

from prompt_toolkit import HTML, print_formatted_text
from prompt_toolkit.styles import Style

from opthub_client.api import TrialStatus
from opthub_client.models.trial import Trial


def user_interaction_message_style() -> Style:
    """Style for user interaction message.

    Returns:
        Style: The prompt-toolkit style object.
    """
    return Style.from_dict(
        {
            "header": "bold cyan",
            "status-evaluating": "bold yellow",
            "status-evaluator_failed": "bold red",
            "status-scoring": "bold yellow",
            "status-scorer_failed": "bold red",
            "status-success": "bold green",
            "section": "bold yellow",
            "key": "bold",
            "value": "",
            "feasible": "bold green ",
            "infeasible": "bold red",
            "error": "bold red",
            "n": "fg:blue bold",
            "e": "fg:red bold",
        },
    )


def display_trial(trial: Trial | None, is_detail: bool) -> None:
    """Display the trial.

    Args:
        trial (Optional[Trial]): The trial to display.
        is_detail (bool): Whether to show detailed information.
    """
    if trial is None:
        print_formatted_text(
            HTML("<error>No more solutions to display.</error>"),
            style=user_interaction_message_style(),
        )
    else:
        lines = get_trial_info_detail(trial) if is_detail else get_trial_info_general(trial)
        print_formatted_text(HTML(lines), style=user_interaction_message_style())


def display_trials(trials: list[Trial], is_detail: bool) -> None:
    """Display the trials.

    Args:
        trials (List[Trial]): The list of trials to display.
        is_detail (bool): Whether to show detailed information for each trial.
    """
    if not trials:
        print_formatted_text(HTML("<error>No solutions to display.</error>"), style=user_interaction_message_style())
    else:
        lines = ""
        for trial in trials:
            lines += get_trial_info_detail(trial) if is_detail else get_trial_info_general(trial)
        print_formatted_text(HTML(lines), style=user_interaction_message_style())


def display_general_status(stats: str | TrialStatus) -> str:
    """Get the status of the trial.

    Args:
        stats (Union[str, TrialStatus]): The trial status.

    Returns:
        str: The human-readable status.
    """
    status_dict = {
        "evaluating": "Evaluating",
        "evaluator_failed": "Failed    ",
        "scoring": "Scoring   ",
        "scorer_failed": "Failed    ",
        "success": "Success   ",
    }
    return status_dict.get(stats, "Unknown")


def display_detail_status(stats: str | TrialStatus) -> str:
    """Get the status of the trial.

    Args:
        stats (Union[str, TrialStatus]): The trial status.

    Returns:
        str: The human-readable status.
    """
    status_dict = {
        "evaluating": "Evaluating",
        "evaluator_failed": "Failed to evaluate",
        "scoring": "Scoring",
        "scorer_failed": "Failed to score",
        "success": "Success",
    }
    return status_dict.get(stats, "Unknown")


def display_feasible(feasible: bool) -> str:
    """Get the feasibility of the trial.

    Args:
        feasible (bool): The feasibility of the trial.

    Returns:
        str: The human-readable feasibility.
    """
    return "<feasible>Feasible</feasible>" if feasible else "<infeasible>Infeasible</infeasible>"


def display_localized_date(iso_date: str) -> str:
    """Convert the ISO 8601 date string to the localized date.

    Args:
        iso_date (str): The ISO 8601 date string.

    Returns:
        str: The localized date string.
    """
    utc_time = datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=UTC)
    local_time = utc_time.astimezone()
    return local_time.strftime("%Y-%m-%d %H:%M:%S %Z")


def user_interaction_message() -> str:
    """User interaction message for show trials."""
    return '<n style="class:n">n</n>: next solutions, <e style="class:e">e</e>: exit \n'


def get_trial_info_general(trial: Trial) -> str:
    """Get the general information of a trial.

    Args:
        trial (Trial): The trial to display.

    Returns:
        str: The general information of the trial.
    """
    score = trial.get("score")
    status = trial.get("status")
    trial_no = trial.get("trialNo")
    lines = ""
    lines += f"<key>Trial No:</key> <value>{trial_no}</value>, "
    lines += f"<status-{status} >{display_general_status(status)}</status-{status}>"
    if score:
        lines += f", <key>Score:</key> <value>{score.get('value')}</value>\n"
    return lines


def get_trial_info_detail(trial: Trial) -> str:
    """Get the detailed information of a trial.

    Args:
        trial (Trial): The trial to display.

    Returns:
        str: The detailed information of the trial.
    """
    lines = f"<header>========== Trial No. {trial.get('trialNo')} ==========</header>\n"
    lines += f"<key>Status:</key> <status-{trial['status']}>{display_detail_status(trial.get('status'))}</status-{trial['status']}>\n\n"  # noqa: E501

    # Solution section
    solution = trial.get("solution", {})
    lines += "<section>Solution:</section>\n"
    lines += f"\t<key>Variable   : </key> <value>{solution.get('variable')}</value>\n"
    lines += f"\t<key>Created At : </key> <value>{display_localized_date(solution.get('created_at', ''))}</value>\n\n"

    # Evaluation section
    evaluation = trial.get("evaluation", {})
    if evaluation:
        lines += "<section>Evaluation:</section>\n"
        lines += f"\t<key>Feasibility         :</key> <value>{display_feasible(evaluation.get('feasible'))}</value>\n"
        lines += f"\t<key>Objective Function  :</key> <value>{evaluation.get('objective')}</value>\n"
        lines += f"\t<key>Constraint Function :</key> <value>{evaluation.get('constraint')}</value>\n"
        lines += f"\t<key>Started At          :</key> <value>{display_localized_date(evaluation.get('started_at', ''))}</value>\n"  # noqa: E501
        lines += f"\t<key>Finished At         :</key> <value>{display_localized_date(evaluation.get('finished_at', ''))}</value>\n\n"  # noqa: E501

    # Score section
    score = trial.get("score", {})
    if score:
        lines += "<section>Score:</section>\n"
        lines += f"\t<key>Value       :</key> <value>{score.get('value')}</value>\n"
        lines += f"\t<key>Started At  :</key> <value>{display_localized_date(score.get('started_at', ''))}</value>\n"
        lines += f"\t<key>Finished At :</key> <value>{display_localized_date(score.get('finished_at', ''))}</value>\n\n"

    # Error details
    error = evaluation.get("error") or score.get("error")
    if error:
        lines += "<error>Error Details:</error>\n"
        lines += "--------------------------------------------------\n"
        lines += f"<value>{error}</value>\n"
        lines += "--------------------------------------------------\n"

    lines += "\n"
    return lines
