"""
Interactive mode file for Git Py Stats
"""

from typing import Dict, Union

from git_py_stats import generate_cmds, list_cmds, suggest_cmds, calendar_cmds
from git_py_stats.menu import interactive_menu


# TODO: We can probably refactor this a bit.
#       Make some sort of exec_cmd to handle a lot
#       of the lambda calls
def handle_interactive_mode(config: Dict[str, Union[str, int]]) -> None:
    """
    Handle the interactive mode using the interactive menu.

    Args:
        config: Dict[str, Union[str, int]]: Config dictionary holding env vars.

    Returns:
        None
    """
    interactive_map = {
        "1": lambda: generate_cmds.detailed_git_stats(config),
        "2": lambda: generate_cmds.detailed_git_stats(config, input("Enter branch name: ")),
        "3": lambda: generate_cmds.changelogs(config),
        "4": lambda: generate_cmds.changelogs(config, input("Enter author name: ")),
        "5": lambda: generate_cmds.my_daily_status(config),
        "6": lambda: generate_cmds.output_daily_stats_csv(config),
        "7": lambda: generate_cmds.save_git_log_output_json(config),
        "8": lambda: list_cmds.branch_tree(config),
        "9": lambda: list_cmds.branches_by_date(config),
        "10": lambda: list_cmds.contributors(config),
        "11": lambda: list_cmds.new_contributors(config, input("Enter cutoff date (YYYY-MM-DD): ")),
        "12": lambda: list_cmds.git_commits_per_author(config),
        "13": lambda: list_cmds.git_commits_per_date(config),
        "14": lambda: list_cmds.git_commits_per_month(config),
        "15": lambda: list_cmds.git_commits_per_year(config),
        "16": lambda: list_cmds.git_commits_per_weekday(config),
        "17": lambda: list_cmds.git_commits_per_weekday(config, input("Enter author name: ")),
        "18": lambda: list_cmds.git_commits_per_hour(config),
        "19": lambda: list_cmds.git_commits_per_hour(config, input("Enter author name: ")),
        "20": lambda: list_cmds.git_commits_per_timezone(config),
        "21": lambda: list_cmds.git_commits_per_timezone(config, input("Enter author name: ")),
        "22": lambda: suggest_cmds.suggest_reviewers(config),
        "23": lambda: calendar_cmds.commits_calendar_by_author(
            config, input("Enter author name: ")
        ),
        "24": lambda: calendar_cmds.commits_heatmap(config),
    }

    while True:
        choice = interactive_menu(config)
        if choice == "" or choice.lower() in ("quit", "exit"):
            break

        action = interactive_map.get(choice)
        if action:
            action()
        else:
            print("Invalid selection. Please try again.")
