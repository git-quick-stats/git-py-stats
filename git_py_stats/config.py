"""
Handles reading configuration settings from environment variables.
"""

import os
from datetime import datetime
from typing import Dict, Union, Optional
from git_py_stats.git_operations import run_git_command

# TODO: This is a rough equivalent of what the original program does.
#       However, that doesn't mean this is the correct way to handle
#       this type of operation since these are not much different
#       from global vars. Granted, they're global in the user's shell env
#       to begin with, but since we now have the power of Python, we can
#       probably handle this in a more expressive way.
#       Context and Decorators? Command Factory to leverage Dependency
#       Injection and the Command pattern? Centralized Config Manager?
#       Marked as future possible refactor.
def get_config() -> Dict[str, Union[str, int]]:
    """
    Reads configuration from environment variables and sets default values.
    These are the original program's environment variables:

    Environment Variables:
        _GIT_SINCE (str): Equivalent to git's --since flag. 
            If not set, defaults to the first commit date in the repository.
        _GIT_UNTIL (str): Equivalent to git's --until flag. 
            If not set, defaults to the current system date/time upon exec
            of the program.
        _GIT_PATHSPEC (str): Specifies files or directories to include/exclude in stats. 
            Defaults to "--" which means to skip over this option.
        _GIT_MERGE_VIEW (str): Merge commit view strategy. Options:
            - 'exclusive' to show only merge commits.
            - 'enable' to use the user's default merge view from the conf.
               Default is usually to show both regular and merge commits.
            - Any other value defaults to '--no-merges' currently.
        _GIT_LIMIT (int): Limits the git log output. Defaults to 10.
        _GIT_LOG_OPTIONS (str): Additional git log options. Default is empty.
        _MENU_THEME (str): Toggles between the default theme and legacy theme.
            - 'legacy' to set the legacy theme
            - Empty to set the default theme

    Returns:
        Dict[str, Union[str, int]]: A dictionary containing the configuration options:
            - 'since' (str): Git command option for the start date.
            - 'until' (str): Git command option for the end date.
            - 'pathspec' (str): Git command option for pathspec.
            - 'merges' (str): Git command option for merge commit view strategy.
            - 'limit' (int): Git log output limit.
            - 'log_options' (str): Additional git log options.
            - 'menu_theme' (str): Menu theme color.
    """
    config: Dict[str, Union[str, int]] = {}

    # _GIT_SINCE
    git_since: Optional[str] = os.environ.get('_GIT_SINCE')
    if git_since:
        config['since'] = f"--since={git_since}"
    else:
        # Get the earliest commit date in the repo
        earliest_commit_date: Optional[str] = run_git_command(['git', 'log', '--reverse', '--format=%ad'])
        if earliest_commit_date:
            first_commit_date: str = earliest_commit_date.split('\n')[0]
            config['since'] = f"--since='{first_commit_date}'"
        else:
            config['since'] = ''

    # _GIT_UNTIL
    git_until: Optional[str] = os.environ.get('_GIT_UNTIL')
    if git_until:
        config['until'] = f"--until={git_until}"
    else:
        # Get the current date/time upon exec of the program
        now: str = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %Z')
        config['until'] = f"--until='{now}'"

    # _GIT_PATHSPEC
    git_pathspec: Optional[str] = os.environ.get('_GIT_PATHSPEC')
    if git_pathspec:
        config['pathspec'] = f"-- {git_pathspec}"
    else:
        config['pathspec'] = "--"

    # _GIT_MERGE_VIEW
    git_merge_view: str = os.environ.get('_GIT_MERGE_VIEW', '').lower()
    if git_merge_view == 'exclusive':
        config['merges'] = '--merges'
    elif git_merge_view == 'enable':
        config['merges'] = ''
    else:
        config['merges'] = '--no-merges'

    # _GIT_LIMIT
    git_limit: Optional[str] = os.environ.get('_GIT_LIMIT')
    if git_limit:
        # Slight sanitization, but we're still gonna wild west this a bit
        try:
            config['limit'] = int(git_limit)
        except ValueError:
            print("Invalid value for _GIT_LIMIT. Using default value 10.")
            config['limit'] = 10
    else:
        config['limit'] = 10

    # _GIT_LOG_OPTIONS
    # NOTE: We'll need to sanitize our entire git command
    git_log_options: Optional[str] = os.environ.get('_GIT_LOG_OPTIONS')
    if git_log_options:
        config['log_options'] = git_log_options
    else:
        config['log_options'] = ''
    
    # _MENU_THEME
    menu_theme: Optional[str] = os.environ.get('_MENU_THEME')
    if menu_theme == 'legacy':
        config['menu_theme'] = 'legacy'
    else:
        config['menu_theme'] = ''

    return config
