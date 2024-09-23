from argparse import ArgumentParser, RawTextHelpFormatter

from git_py_stats import generate_cmds
from git_py_stats import list_cmds
from git_py_stats import suggest_cmds


def handle_non_interactive_mode(args) -> None:
    """
    Handle the non-interactive mode based on command-line arguments.

    Args:
        args: Parsed command-line arguments.
    """
    non_interactive_map = {
        'detailed_git_stats': generate_cmds.contribution_stats_by_author,
        'git_stats_by_branch': lambda: generate_cmds.contribution_stats_by_author(args.git_stats_by_branch),
        'changelogs': generate_cmds.changelogs,
        'changelogs_by_author': lambda: generate_cmds.changelogs(args.changelogs_by_author),
        'my_daily_stats': generate_cmds.my_daily_status,
        'csv_output_by_branch': generate_cmds.output_daily_stats_csv,
        'json_output': generate_cmds.save_git_log_output_json,
        'branch_tree': list_cmds.branch_tree,
        'branches_by_date': list_cmds.branches_by_date,
        'contributors': list_cmds.contributors,
        'new_contributors': lambda: list_cmds.new_contributors(args.new_contributors),
        'commits_per_author': list_cmds.git_commits_per_author,
        'commits_per_day': list_cmds.git_commits_per_date,
        'commits_by_year': list_cmds.git_commits_per_year,
        'commits_by_month': list_cmds.git_commits_per_month,
        'commits_by_weekday': list_cmds.git_commits_per_weekday,
        'commits_by_author_by_weekday': lambda: list_cmds.git_commits_per_weekday(args.commits_by_author_by_weekday),
        'commits_by_hour': list_cmds.git_commits_per_hour,
        'commits_by_author_by_hour': lambda: list_cmds.git_commits_per_hour(args.commits_by_author_by_hour),
        'commits_by_timezone': list_cmds.git_commits_per_timezone,
        'commits_by_author_by_timezone': lambda: list_cmds.git_commits_per_timezone(args.commits_by_author_by_timezone),
        'suggest_reviewers': suggest_cmds.suggest_reviewers,
    }

    # Call the appropriate function based on the command-line argument
    for arg, function in non_interactive_map.items():
        if getattr(args, arg):
            function()
            return

    # Invalid options handling
    print("Invalid option provided.\n")
    parser = ArgumentParser(
        description='Git Py Stats',
        formatter_class=RawTextHelpFormatter
    )
    parser.print_help()

