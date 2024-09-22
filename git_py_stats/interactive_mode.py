from git_py_stats import generate_cmds
from git_py_stats import list_cmds
from git_py_stats import suggest_cmds
from git_py_stats.menu import interactive_menu

def handle_interactive_mode() -> None:
    """
    Handle the interactive mode using the interactive menu.
    """
    interactive_map = {
        '1': generate_cmds.contribution_stats_by_author,
        '2': lambda: generate_cmds.contribution_stats_by_author(input("Enter branch name: ")),
        '3': generate_cmds.git_changelogs_last_10_days,
        '4': lambda: generate_cmds.git_changelogs_last_10_days(input("Enter author name: ")),
        '5': generate_cmds.my_daily_status,
        '6': generate_cmds.output_daily_stats_csv,
        '7': generate_cmds.save_git_log_output_json,
        '8': list_cmds.branch_tree_view,
        '9': list_cmds.all_branches_sorted,
        '10': list_cmds.all_contributors,
        '11': list_cmds.new_contributors,
        '12': list_cmds.git_commits_per_author,
        '13': list_cmds.git_commits_per_date,
        '14': list_cmds.git_commits_per_month,
        '15': list_cmds.git_commits_per_year,
        '16': list_cmds.git_commits_per_weekday,
        '17': lambda: list_cmds.git_commits_per_weekday(input("Enter author name: ")),
        '18': list_cmds.git_commits_per_hour,
        '19': lambda: list_cmds.git_commits_per_hour(input("Enter author name: ")),
        '20': list_cmds.git_commits_per_timezone,
        '21': lambda: list_cmds.git_commits_per_timezone(input("Enter author name: ")),
        '22': suggest_cmds.code_reviewers,
    }

    while True:
        choice = interactive_menu()
        if choice == '' or choice.lower() in ('quit', 'exit'):
            break

        action = interactive_map.get(choice)
        if action:
            action()
        else:
            print("Invalid selection. Please try again.")

