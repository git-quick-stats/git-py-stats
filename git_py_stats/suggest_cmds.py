"""
Performs all commands in the Suggest section of the program.
"""

import subprocess
from collections import defaultdict
from typing import Dict, Union

from git_py_stats.git_operations import run_git_command


def suggest_reviewers(config: Dict[str, Union[str, int]]) -> None:
    """
    Suggests potential code reviewers based on commit history.

    Args:
        config: Dict[str, Union[str, int]]: Config dictionary holding env vars.

    Returns:
        None
    """

    # Construct the git log command with all options. Original command is:
    # git -c log.showSignature=false log --use-mailmap $_merges "$_since" "$_until" \
    #     --pretty=%aN $_log_options $_pathspec | head -n 100 | sort | uniq -c \
    #     | sort -nr
    # Then some LC_ALL portion which is currently not important
    # Then pipe it all into column -t -s

    # Grab the config options from our config.py.
    # config.py should give fallbacks for these, but for sanity, lets
    # also provide some defaults just in case.
    merges = config.get("merges", "--no-merges")
    since = config.get("since", "")
    until = config.get("until", "")
    log_options = config.get("log_options", "")
    pathspec = config.get("pathspec", "")

    cmd = [
        "git",
        "-c",
        "log.showSignature=false",
        "log",
        "--use-mailmap",
        merges,
        since,
        until,
        "--pretty=%aN",
        log_options,
        pathspec,
    ]

    # Remove any empty space from the cmd
    cmd = [arg for arg in cmd if arg]

    try:
        # Execute the git command and get the output
        output = run_git_command(cmd)
        if not output:
            print("No data available.")
            return

        # Split the output into lines (each line is a commit author)
        lines = output.splitlines()

        # Mimic "head -n 100"
        head_lines = lines[:100]

        # Mimic "sort"
        sorted_lines = sorted(head_lines)

        # Mimic "uniq -c"
        counted_authors = []
        current_author = None
        current_count = 0

        # Iterate over sorted lines and count consecutive duplicates
        for author in sorted_lines:
            if author == current_author:
                current_count += 1
            else:
                if current_author is not None:
                    counted_authors.append((current_count, current_author))
                current_author = author
                current_count = 1

        # Append the last counted author
        if current_author is not None:
            counted_authors.append((current_count, current_author))

        # Sort by count descending, and by name ascending
        sorted_authors = sorted(counted_authors, key=lambda x: (-x[0], x[1]))

        # Print results similar to "column -t -s"
        if sorted_authors:
            print("Suggested code reviewers based on git history:")
            for count, author in sorted_authors:
                # Pad output with 7 to match original code's behavior
                # TODO: Bit of a magic number we can remove later
                print(f"{count:7} {author}")
        else:
            print("No potential reviewers found.")

    except subprocess.CalledProcessError as e:
        print(f"Error executing git command: {e}")
