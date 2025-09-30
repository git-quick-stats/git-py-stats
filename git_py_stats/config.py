"""
Handles reading configuration settings from environment variables.
"""

import os
import re
from datetime import datetime
from typing import Dict, Union, Optional, Callable
from git_py_stats.git_operations import run_git_command


def _build_author_exclusion_filter(pattern: str) -> Callable[[str], bool]:
    """
    Compile a string of authors that tells you whether an author
    should be ignored based on a user-configured environment
    variable.

    Args:
        pattern (str): A regex (Example: "(user@example.com|Some User)").
                       No flags are injected automatically, but users can
                       include them for case-insensitive matches.

    Returns:
        Callable[[str], bool]: Input string 's' that matches the pattern to be
                               ignored. False otherwise.
    """
    pattern = (pattern or "").strip()
    if not pattern:
        return lambda _s: False
    rx = re.compile(pattern)
    return lambda s: bool(rx.search(s or ""))


def _parse_git_sort_by(raw: str) -> tuple[str, str]:
    """
    Helper function for handling sorting features for contribution stats.
    Handles the following metrics:
      - "name" (default)
      - "commits"
      - "insertions"
      - "deletions"
      - "lines"
    Handles the following directions:
      - "asc" (default)
      - "desc"

    Args:
        Raw string

    Returns:
        metric (str): The metric to sort by
        direction (str): Whether we want ascending or descending
    """
    allowed_metrics = {"name", "commits", "insertions", "deletions", "lines"}
    metric = "name"
    direction = "asc"

    if not raw:
        return metric, direction

    parts = raw.strip().lower().split("-", 1)
    if parts:
        m = parts[0].strip()
        if m in allowed_metrics:
            metric = m
        else:
            print(f"WARNING: Invalid sort metric '{m}' set in _GIT_SORT_BY.", end=" ")
            print("Falling back to 'name'.")
    if len(parts) == 2:
        d = parts[1].strip()
        if d in {"asc", "desc"}:
            direction = d
        else:
            print(f"WARNING: Invalid sort direction '{m}' in _GIT_SORT_BY.", end=" ")
            print("Falling back to 'asc'.")

    return metric, direction


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
        _GIT_BRANCH (str): Sets branch you want to target for some stats.
            Default is empty which falls back to the current branch you're on.
        _GIT_LIMIT (int): Limits the git log output. Defaults to 10.
        _GIT_LOG_OPTIONS (str): Additional git log options. Default is empty.
        _GIT_DAYS (int): Defines number of days for the heatmap. Default is empty.
        _GIT_SORT_BY (str): Defines sort metric and direction for contribution stats.
                            Default is name-asc.
        _GIT_IGNORE_AUTHORS (str): Defines authors to ignore. Default is empty.
        _MENU_THEME (str): Toggles between the default theme and legacy theme.
            - 'legacy' to set the legacy theme
            - 'none' to disable the menu theme
            - Empty to set the default theme

    Args:
        None

    Returns:
        Dict[str, Union[str, int]]: A dictionary containing the configuration options:
            - 'since' (str): Git command option for the start date.
            - 'until' (str): Git command option for the end date.
            - 'pathspec' (str): Git command option for pathspec.
            - 'merges' (str): Git command option for merge commit view strategy.
            - 'branch' (str): Git branch name.
            - 'limit' (int): Git log output limit.
            - 'log_options' (str): Additional git log options.
            - 'days' (str): Number of days for the heatmap.
            - 'sort_by' (str): Sort by field and sort direction (asc/desc).
            - 'ignore_authors': (str): Any author(s) to ignore.
            - 'menu_theme' (str): Menu theme color.
    """
    config: Dict[str, Union[str, int]] = {}

    # _GIT_SINCE
    git_since: Optional[str] = os.environ.get("_GIT_SINCE")
    if git_since:
        config["since"] = f"--since={git_since}"
    else:
        # Get the earliest commit date in the repo
        earliest_commit_date: Optional[str] = run_git_command(
            ["git", "log", "--reverse", "--format=%ad"]
        )
        if earliest_commit_date:
            first_commit_date: str = earliest_commit_date.split("\n")[0]
            config["since"] = f"--since='{first_commit_date}'"
        else:
            config["since"] = ""

    # _GIT_UNTIL
    git_until: Optional[str] = os.environ.get("_GIT_UNTIL")
    if git_until:
        config["until"] = f"--until={git_until}"
    else:
        # Get the current date/time upon exec of the program
        now: str = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z")
        config["until"] = f"--until='{now}'"

    # _GIT_PATHSPEC
    git_pathspec: Optional[str] = os.environ.get("_GIT_PATHSPEC")
    if git_pathspec:
        config["pathspec"] = f"-- {git_pathspec}"
    else:
        config["pathspec"] = "--"

    # _GIT_MERGE_VIEW
    git_merge_view: str = os.environ.get("_GIT_MERGE_VIEW", "").lower()
    if git_merge_view == "exclusive":
        config["merges"] = "--merges"
    elif git_merge_view == "enable":
        config["merges"] = ""
    else:
        config["merges"] = "--no-merges"

    # _GIT_BRANCH
    git_branch: Optional[str] = os.environ.get("_GIT_BRANCH")
    if git_branch:
        config["branch"] = git_branch
    else:
        config["branch"] = ""

    # _GIT_LIMIT
    git_limit: Optional[str] = os.environ.get("_GIT_LIMIT")
    if git_limit:
        # Slight sanitization, but we're still gonna wild west this a bit
        try:
            config["limit"] = int(git_limit)
        except ValueError:
            print("Invalid value for _GIT_LIMIT. Using default value 10.")
            config["limit"] = 10
    else:
        config["limit"] = 10

    # _GIT_LOG_OPTIONS
    # NOTE: We'll need to sanitize our entire git command
    git_log_options: Optional[str] = os.environ.get("_GIT_LOG_OPTIONS")
    if git_log_options:
        config["log_options"] = git_log_options
    else:
        config["log_options"] = ""

    # _GIT_DAYS
    git_days: Optional[str] = os.environ.get("_GIT_DAYS")
    if git_days:
        # Slight sanitization, but we're still gonna wild west this a bit
        try:
            config["days"] = int(git_days)
        except ValueError:
            print("Invalid value for _GIT_DAYS. Using default value 30.")
            config["days"] = 30
    else:
        config["days"] = 30

    # _GIT_SORT_BY
    _git_sort_by_raw = os.environ.get("_GIT_SORT_BY", "")
    sort_by, sort_dir = _parse_git_sort_by(_git_sort_by_raw)
    config["sort_by"] = sort_by
    config["sort_dir"] = sort_dir

    # _GIT_IGNORE_AUTHORS
    ignore_authors_pattern: Optional[str] = os.environ.get("_GIT_IGNORE_AUTHORS")
    config["ignore_authors"] = _build_author_exclusion_filter(ignore_authors_pattern)

    # _MENU_THEME
    menu_theme: Optional[str] = os.environ.get("_MENU_THEME")
    if menu_theme == "legacy":
        config["menu_theme"] = "legacy"
    elif menu_theme == "none":
        config["menu_theme"] = "none"
    else:
        config["menu_theme"] = ""

    return config
