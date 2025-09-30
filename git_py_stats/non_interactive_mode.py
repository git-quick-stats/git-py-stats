"""
Handles the non-interactive mode for Git Py Stats
"""

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from typing import Dict, Union

from git_py_stats import generate_cmds, list_cmds, suggest_cmds, calendar_cmds


def handle_non_interactive_mode(args: Namespace, config: Dict[str, Union[str, int]]) -> None:
    """
    Handle the non-interactive mode based on command-line arguments.

    Args:
        args: Namespace: Parsed command-line arguments.
        config: Dict[str, Union[str, int]]: Config dictionary holding env vars.

    Returns:
        None
    """
    non_interactive_map = {
        "detailed_git_stats": lambda: generate_cmds.detailed_git_stats(config),
        "git_stats_by_branch": lambda: generate_cmds.detailed_git_stats(
            config, args.git_stats_by_branch
        ),
        "changelogs": lambda: generate_cmds.changelogs(config),
        "changelogs_by_author": lambda: generate_cmds.changelogs(config, args.changelogs_by_author),
        "my_daily_stats": lambda: generate_cmds.my_daily_status(config),
        "csv_output_by_branch": lambda: generate_cmds.output_daily_stats_csv(config),
        "json_output": lambda: generate_cmds.save_git_log_output_json(config),
        "branch_tree": lambda: list_cmds.branch_tree(config),
        "branches_by_date": lambda: list_cmds.branches_by_date(config),
        "contributors": lambda: list_cmds.contributors(config),
        "new_contributors": lambda: list_cmds.new_contributors(config, args.new_contributors),
        "commits_per_author": lambda: list_cmds.git_commits_per_author(config),
        "commits_per_day": lambda: list_cmds.git_commits_per_date(config),
        "commits_by_year": lambda: list_cmds.git_commits_per_year(config),
        "commits_by_month": lambda: list_cmds.git_commits_per_month(config),
        "commits_by_weekday": lambda: list_cmds.git_commits_per_weekday(config),
        "commits_by_author_by_weekday": lambda: list_cmds.git_commits_per_weekday(
            config, args.commits_by_author_by_weekday
        ),
        "commits_by_hour": lambda: list_cmds.git_commits_per_hour(config),
        "commits_by_author_by_hour": lambda: list_cmds.git_commits_per_hour(
            config, args.commits_by_author_by_hour
        ),
        "commits_by_timezone": lambda: list_cmds.git_commits_per_timezone(config),
        "commits_by_author_by_timezone": lambda: list_cmds.git_commits_per_timezone(
            config, args.commits_by_author_by_timezone
        ),
        "suggest_reviewers": lambda: suggest_cmds.suggest_reviewers(config),
        "commits_calendar_by_author": lambda: calendar_cmds.commits_calendar_by_author(
            config, args.commits_calendar_by_author
        ),
        "commits_heatmap": lambda: calendar_cmds.commits_heatmap(config),
    }

    # Call the appropriate function based on the command-line argument
    for arg, function in non_interactive_map.items():
        if getattr(args, arg):
            function()
            return

    # Invalid options handling
    print("Invalid option provided.\n")
    parser = ArgumentParser(description="Git Py Stats", formatter_class=RawTextHelpFormatter)
    parser.print_help()
