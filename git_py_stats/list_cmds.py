"""
Functions related to the 'List' section.
"""

import collections
import re
from datetime import datetime
from typing import Dict, Union, Optional

from git_py_stats.git_operations import run_git_command


def branch_tree(config: Dict[str, Union[str, int]]) -> None:
    """
    Displays a visual graph of recent commits across all branches.

    Args:
        config: Dict[str, Union[str, int]]: Config dictionary holding env vars.

    Returns:
        None
    """

    # Grab the config options from our config.py.
    # config.py should give fallbacks for these, but for sanity, lets
    # also provide some defaults just in case.
    since = config.get("since", "")
    until = config.get("until", "")
    log_options = config.get("log_options", "")
    limit = config.get("limit", 10)

    # Format string for git --format so it gets interpreted correctly
    format_str = (
        "--format=--+ Commit:  %h%n  | Date:    %aD (%ar)%n  | "
        "Message: %s %d%n  + Author:  %aN %n"
    )

    # Original command:
    # git -c log.showSignature=false log --use-mailmap --graph --abbrev-commit \
    #     "$_since" "$_until" --decorate \
    #      --format=format:'--+ Commit:  %h %n  | Date:    %aD (%ar) %n''  \
    #                       | Message: %s %d %n''  + Author:  %aN %n' \
    #      --all $_log_options | head -n $((_limit*5))
    cmd = [
        "git",
        "-c",
        "log.showSignature=false",
        "log",
        "--use-mailmap",
        "--graph",
        "--abbrev-commit",
        since,
        until,
        "--decorate",
        format_str,
        "--all",
        log_options,
    ]

    # Remove any empty space from the cmd
    cmd = [arg for arg in cmd if arg]

    output = run_git_command(cmd)

    # handle the head -n $((_limit*5)) portion
    if output:
        print("Branching tree view:\n")
        lines = output.split("\n")
        total_lines = limit * 5
        limited_lines = lines[:total_lines]

        for line in limited_lines:
            print(f"{line}")

        # commit_count = sum(
        #    1 for line in limited_lines if line.strip().startswith("--+ Commit:")
        # )
    else:
        print("No data available.")


def branches_by_date(config: Dict[str, Union[str, int]]) -> None:
    """
    Lists branches sorted by the latest commit date.

    Args:
        config: Dict[str, Union[str, int]]: Config dictionary holding env vars.

    Returns:
        None
    """

    # Grab the config options from our config.py.
    ignore_authors = config.get("ignore_authors", lambda _s: False)

    # Original command:
    # git for-each-ref --sort=committerdate refs/heads/ \
    #     --format='[%(authordate:relative)] %(authorname) %(refname:short)' | cat -n
    # TODO: Wouldn't git log --pretty=format:'%ad' --date=short be better here?
    #       Then we could pipe it through sort, uniq -c, sort -nr, etc.
    #       Possibly feed back into the parent project

    # Include the email so we can filter based off it, but keep the visible
    # part the same as before.
    visible_fmt = "[%(authordate:relative)] %(authorname) %(refname:short)"
    format_str = f"{visible_fmt}|%(authoremail)"

    cmd = [
        "git",
        "for-each-ref",
        "--sort=committerdate",
        "refs/heads/",
        f"--format={format_str}",
    ]

    output = run_git_command(cmd)
    if not output:
        print("No commits found.")
        return

    # Split lines and filter by author (both name and email), but keep
    # visible text only.
    visible_lines = []
    for raw in output.split("\n"):
        if not raw.strip():
            continue
        if "|" in raw:
            visible, email = raw.split("|", 1)
        else:
            visible, email = raw, ""

        # Filter by either email or the visible chunk.
        if ignore_authors(email) or ignore_authors(visible):
            continue

        visible_lines.append(visible)

    if not visible_lines:
        print("No commits found.")
        return

    # Number like `cat -n`
    print("All branches (sorted by most recent commit):\n")
    for idx, line in enumerate(visible_lines, 1):
        print(f"\t{idx}  {line}")


def contributors(config: Dict[str, Union[str, int]]) -> None:
    """
    Lists all contributors alphabetically.

    Args:
        config: Dict[str, Union[str, int]]: Config dictionary holding env vars.

    Returns:
        None
    """

    # Grab the config options from our config.py.
    # config.py should give fallbacks for these, but for sanity, lets
    # also provide some defaults just in case.
    merges = config.get("merges", "--no-merges")
    since = config.get("since", "")
    until = config.get("until", "")
    log_options = config.get("log_options", "")
    pathspec = config.get("pathspec", "")
    limit = config.get("limit", 10)

    # Original command
    #     git -c log.showSignature=false log --use-mailmap $_merges "$_since" "$_until" \
    #         --format='%aN' $_log_options $_pathspec | sort -u | cat -n
    cmd = [
        "git",
        "-c",
        "log.showSignature=false",
        "log",
        "--use-mailmap",
        merges,
        since,
        until,
        "--format=%aN",
        log_options,
        pathspec,
    ]

    # Remove any empty space from the cmd
    cmd = [arg for arg in cmd if arg]

    output = run_git_command(cmd)
    if output:
        print("All contributors (sorted by name):\n")
        # Split the output into individual author names
        authors = [line.strip() for line in output.split("\n") if line.strip()]

        # Remove duplicates by converting the list to a set
        unique_authors = set(authors)

        # Sort the unique authors alphabetically
        sorted_authors = sorted(unique_authors)

        # Apply the limit
        limited_authors = sorted_authors[:limit]

        # Number the authors similar to 'cat -n' and print
        numbered_authors = [f"{idx + 1}  {author}" for idx, author in enumerate(limited_authors)]
        for author in numbered_authors:
            print(f"\t{author}")
    else:
        print("No contributors found.")


def new_contributors(config: Dict[str, Union[str, int]], new_date: str) -> None:
    """
    Lists all new contributors to a repo since the specified date.

    Args:
        config: Dict[str, Union[str, int]]: Config dictionary holding env vars.
        new_date (str): Cutoff date for being considered "new" in 'YYYY-MM-DD' format.

    Returns:
        None
    """

    # Attempt to handle date in YYYY-MM-DD format
    try:
        new_date_dt = datetime.strptime(new_date, "%Y-%m-%d")
        new_date_ts = int(new_date_dt.timestamp())
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    # Grab the config options from our config.py.
    # config.py should give fallbacks for these, but for sanity, lets
    # also provide some defaults just in case.
    merges = config.get("merges", "--no-merges")
    since = config.get("since", "")
    until = config.get("until", "")
    log_options = config.get("log_options", "")
    pathspec = config.get("pathspec", "")
    ignore_authors = config.get("ignore_authors", lambda _s: False)

    # Original command:
    # git -c log.showSignature=false log --use-mailmap $_merges \
    #     "$_since" "$_until" --format='%aE' $_log_options \
    #     $_pathspec | sort -u
    cmd = [
        "git",
        "-c",
        "log.showSignature=false",
        "log",
        "--use-mailmap",
        merges,
        since,
        until,
        "--format=%aE|%at",
        log_options,
        pathspec,
    ]

    # Remove any empty strings from the command
    cmd = [arg for arg in cmd if arg]

    output = run_git_command(cmd)
    if output:
        # Dictionary to store the earliest commit timestamp for each contributor
        contributors_dict = {}

        # Process each line of the Git output
        for line in output.split("\n"):
            try:
                email, timestamp = line.split("|")
                timestamp = int(timestamp)
                # Skip ignored by email
                if ignore_authors(email):
                    continue
                # If the contributor is not in the dictionary or the current timestamp is earlier
                if email not in contributors_dict or timestamp < contributors_dict[email]:
                    contributors_dict[email] = timestamp
            except ValueError:
                continue  # Skip lines that don't match format

        # List to hold new contributors
        new_contributors_list = []

        # Iterate over contributors to find those who are new since 'new_date'
        for email, first_commit_ts in contributors_dict.items():
            if first_commit_ts >= new_date_ts:
                # Retrieve the contributor's name
                # Original command:
                # git -c log.showSignature=false log --author="$c" \
                #     --reverse --use-mailmap $_merges "$_since" "$_until" \
                #     --format='%at' $_log_options $_pathspec | head -n 1
                name_cmd = [
                    "git",
                    "-c",
                    "log.showSignature=false",
                    "log",
                    "--author=" + email,
                    "--reverse",
                    "--use-mailmap",
                    since,
                    until,
                    "--format=%aN",
                    log_options,
                    pathspec,
                    "-n",
                    "1",
                ]

                # Remove any empty strings from the command
                name_cmd = [arg for arg in name_cmd if arg]

                # Grab name + email if we can. Otherwise, just grab email
                # while also making sure to ignore any authors that may be
                # in our ignore_author env var
                name = (run_git_command(name_cmd) or "").strip()
                combo = f"{name} <{email}>" if name else f"<{email}>"
                if ignore_authors(email) or ignore_authors(name) or ignore_authors(combo):
                    continue

                new_contributors_list.append((name, email))
        # Sort the list alphabetically by name to match the original
        # and print all of this out
        if new_contributors_list:
            print(f"New contributors since {new_date}:\n")
            sorted_new_contributors = sorted(new_contributors_list, key=lambda x: (x[0], x[1]))
            for idx, (name, email) in enumerate(sorted_new_contributors, 1):
                if name:
                    print(f"{name} <{email}>")
                else:
                    print(f"<{email}>")
        else:
            print("No new contributors found since the specified date.")
    else:
        print("No contributors found.")


def git_commits_per_author(config: Dict[str, Union[str, int]]) -> None:
    """
    Shows the number of commits per author.

    Args:
        config: Dict[str, Union[str, int]]: Config dictionary holding env vars.

    Returns:
        None
    """

    # Grab the config options from our config.py.
    # config.py should give fallbacks for these, but for sanity, lets
    # also provide some defaults just in case.
    merges = config.get("merges", "--no-merges")
    since = config.get("since", "")
    until = config.get("until", "")
    log_options = config.get("log_options", "")
    pathspec = config.get("pathspec", "")

    # Original authors command:
    # git -c log.showSignature=false log --use-mailmap \
    #     $_merges "$_since" "$_until" $_log_options \
    #     | grep -i Author: | cut -c9-

    # Original co-authors command:
    # git -c log.showSignature=false log --author="$c" \
    #     --reverse --use-mailmap $_merges "$_since" "$_until" \
    #     --format='%at' $_log_options $_pathspec | head -n 1
    cmd = [
        "git",
        "-c",
        "log.showSignature=false",
        "log",
        "--use-mailmap",
        merges,
        since,
        until,
        "--pretty=format:Author:%aN <%aE>%n%b",
        log_options,
        pathspec,
    ]

    # Remove any empty space from the cmd
    cmd = [arg for arg in cmd if arg]

    output = run_git_command(cmd)
    if not output:
        print("No commits found.")
        return

    # Initialize commit count dictionary
    commit_counts = {}

    # Total commits (including co-authored commits)
    total_commits = 0

    # Regular expressions for parsing the author(s)
    author_regex = re.compile(r"^Author:\s*(.+)$", re.IGNORECASE)
    coauthor_regex = re.compile(r"^Co-Authored-by:\s*(.+)$", re.IGNORECASE)

    # Process each line of the git output
    for line in output.split("\n"):
        author_match = author_regex.match(line)
        coauthor_match = coauthor_regex.match(line)

        # Handle author
        if author_match:
            author_info = author_match.group(1).strip()
            author_name = extract_name(author_info)
            if author_name:
                commit_counts[author_name] = commit_counts.get(author_name, 0) + 1
                total_commits += 1

        # Handle co-author
        elif coauthor_match:
            coauthor_info = coauthor_match.group(1).strip()
            coauthor_name = extract_name(coauthor_info)
            if coauthor_name:
                commit_counts[coauthor_name] = commit_counts.get(coauthor_name, 0) + 1
                total_commits += 1

    # Handle case if nothing is found
    if total_commits == 0:
        print("No commits found.")
        return

    # Prepare a list of contributors with counts and percentages
    contributors_list = []
    for author, count in commit_counts.items():
        percentage = (count / total_commits) * 100
        contributors_list.append((count, author, percentage))

    # Sort the list by commit count in descending order
    contributors_list.sort(key=lambda x: x[0], reverse=True)

    # Fancy stuff for making the commit count alignment kosher
    max_count = contributors_list[0][0]
    count_width = len(str(max_count)) + 1  # Extra space for alignment

    # Print all the fun stuff. Finally...
    print("Git commits per author:\n")
    for count, author, percentage in contributors_list:
        print(f"\t{count:<{count_width}} {author:<30} {percentage:5.1f}%")


def extract_name(author_info: str) -> Optional[str]:
    """
    Extracts the author's name from the author information string.

    Args:
        author_info (str): The author information string
        (e.g., "Name <email@example.com>").

    Returns:
        Optional[str]: The extracted author name, or None if extraction fails.
    """

    # Use regex to extract the name before the email
    # Mostly a helper function for commits
    # NOTE: Should we move this into a separate file with other helper funcs?
    match = re.match(r"^([^<]+)", author_info)
    if match:
        return match.group(1).strip()
    else:
        return None


def git_commits_per_date(config: Dict[str, Union[str, int]]) -> None:
    """
    Displays commits grouped by date.

    Args:
        config: Dict[str, Union[str, int]]: Config dictionary holding env vars.

    Returns:
        None
    """

    # Grab the config options from our config.py.
    # config.py should give fallbacks for these, but for sanity, lets
    # also provide some defaults just in case.
    merges = config.get("merges", "--no-merges")
    since = config.get("since", "")
    until = config.get("until", "")
    log_options = config.get("log_options", "")
    pathspec = config.get("pathspec", "")

    # Original command
    #  git -c log.showSignature=false log --use-mailmap $_merges "$_since" "$_until" \
    #      --date=short --format='%ad' $_log_options $_pathspec | sort | uniq -c
    cmd = [
        "git",
        "-c",
        "log.showSignature=false",
        "log",
        "--use-mailmap",
        merges,
        since,
        until,
        "--date=short",
        "--pretty=format:%ad",
        log_options,
        pathspec,
    ]

    # Remove any empty space from the cmd
    cmd = [arg for arg in cmd if arg]

    # Print out the commit count and date in YYYY-MM-DD format
    output = run_git_command(cmd)
    if output:
        dates = output.split("\n")
        counter = collections.Counter(dates)
        print("Git commits per date:\n")

        # Need to figure out the max count for width alignment purposes
        max_count = max(counter.values())
        count_width = len(str(max_count))

        # Can now display this to the terminal
        for date, count in sorted(counter.items()):
            print(f"\t{count:>{count_width}} {date}")
    else:
        print("No commits found.")


def git_commits_per_month(config: Dict[str, Union[str, int]]) -> None:
    """
    Displays commits grouped by month.

    Args:
        config: Dict[str, Union[str, int]]: Config dictionary holding env vars.

    Returns:
        None
    """

    # Grab the config options from our config.py.
    # config.py should give fallbacks for these, but for sanity, lets
    # also provide some defaults just in case.
    merges = config.get("merges", "--no-merges")
    since = config.get("since", "")
    until = config.get("until", "")
    log_options = config.get("log_options", "")

    # Define months
    months_order = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    # Initialize counts
    commit_counts = {month: 0 for month in months_order}

    # NOTE: One of the issues is that the scaling factor can be weird
    #       Let's pass this for now, but we want to eventually
    #       make this a user-adjustable field that gets passed
    #       to the function
    max_bar_length = 20

    # Original command:
    #  git -c log.showSignature=false shortlog -n $_merges --format='%ad %s' \
    #      "$_since" "$_until" $_log_options |
    #      grep -cE " \w\w\w $i [0-9]{1,2} "
    # NOTE: We can grab the month via %b
    cmd = [
        "git",
        "-c",
        "log.showSignature=false",
        "log",
        "--use-mailmap",
        merges,
        "--date=format:%b",
        "--pretty=format:%cd",
        since,
        until,
        log_options,
    ]

    # Remove any empty space from the cmd
    cmd = [arg for arg in cmd if arg]

    output = run_git_command(cmd)

    if output:
        print("Git commits by month:\n")
        # Split the output into individual month abbreviations
        months = output.split("\n")
        for month in months:
            if month in commit_counts:
                commit_counts[month] += 1

        # Determine the maximum count to set the scaling factor
        max_count = max(commit_counts.values()) if commit_counts else 0

        # Need this in case we ever divide by zero
        scaling_factor = (max_bar_length / max_count) if max_count > 0 else 0

        # Print the header row
        header_month = "Month"
        header_sum = "Sum"
        print(f"\t{header_month:<6}\t{header_sum:<4}")

        # Iterate through the sorted months and print counts
        for month in months_order:
            count = commit_counts[month]
            if count > 0:
                # Calculate the number of blocks for the bar
                num_blocks = int(count * scaling_factor)
                bar = "|" + "█" * num_blocks
            else:
                # Different from the normal one, but lets
                # Represent months with no commits with a dash
                bar = "-"

            # Print with alignment
            print(f"\t{month:<6}\t{count:<4}\t{bar}")
    else:
        print("No commits found.")


def git_commits_per_year(config: Dict[str, Union[str, int]]) -> None:
    """
    Displays commits grouped by year.

    Args:
        config: Dict[str, Union[str, int]]: Config dictionary holding env vars.

    Returns:
        None
    """

    # Grab the config options from our config.py.
    # config.py should give fallbacks for these, but for sanity, lets
    # also provide some defaults just in case.
    merges = config.get("merges", "--no-merges")
    since = config.get("since", "")
    until = config.get("until", "")
    log_options = config.get("log_options", "")

    # Bar length
    # TODO: Make this user adjustable
    max_bar_length = 30

    # Original command:
    #  git -c log.showSignature=false shortlog -n $_merges --format='%ad %s' \
    #      "$__since" "$__until" $_log_options | grep -cE \
    #      " \w\w\w [0-9]{1,2} [0-9][0-9]:[0-9][0-9]:[0-9][0-9] $year "
    #
    # Note, we can use %Y to grab the year
    cmd = [
        "git",
        "-c",
        "log.showSignature=false",
        "log",
        "--use-mailmap",
        merges,
        "--date=format:%Y",
        "--pretty=format:%cd",
        since,
        until,
        log_options,
    ]

    # Remove any empty space from the cmd
    cmd = [arg for arg in cmd if arg]

    output = run_git_command(cmd)
    if output:
        print("Git commits by year:\n")

        # Split the output into individual years
        # Handle cases in case there are no commits found
        years = output.split("\n")
        years = [year for year in years if year.strip()]
        if not years:
            print("No valid years found in commits.")
            return

        # Count the frequency of each year
        # Handle cases in case years weren't valid
        counter = collections.Counter(years)
        all_years = sorted(counter.keys())
        try:
            start_year = int(all_years[0])
            end_year = int(all_years[-1])
        except (ValueError, IndexError):
            # In case the conversion fails
            print("No valid years found in commits.")
            return

        # Initialize commit counts for all years in range
        commit_counts = {year: 0 for year in range(start_year, end_year + 1)}
        for year, count in counter.items():
            commit_counts[int(year)] = count

        # Calculate total commits
        total_commits = sum(commit_counts.values())
        if total_commits == 0:
            print("No commits found.")
            return

        # Determine the maximum count to set the scaling factor
        max_count = max(commit_counts.values())
        scaling_factor = (max_bar_length / max_count) if max_count > 0 else 0

        # Print the header row
        header_year = "Year"
        header_sum = "Sum"
        print(f"\t{header_year:<6}\t{header_sum:<4}")

        # Iterate through the sorted years and print
        for year in range(start_year, end_year + 1):
            count = commit_counts.get(year, 0)
            if count > 0:
                num_blocks = int(count * scaling_factor)
                num_blocks = min(num_blocks, max_bar_length)
                bar = "|" + "█" * num_blocks
            else:
                # Represent years with no commits with a dash
                bar = "-"
            print(f"\t{year:<6}\t{count:<4}\t{bar}")
    else:
        print("No commits found.")


def git_commits_per_weekday(
    config: Dict[str, Union[str, int]], author: Optional[str] = None
) -> None:
    """
    Shows commits grouped by weekday. If an author is provided, it shows
    commits grouped by weekday for that specific author.

    Args:
        config: Dict[str, Union[str, int]]: Config dictionary holding env vars.
        author (Optional[str]): The author you want to show the commits grouped by.
        If None, show for all authors.

    Returns:
        None
    """
    # Grab the config options from our config.py.
    # config.py should give fallbacks for these, but for sanity, lets
    # also provide some defaults just in case.
    merges = config.get("merges", "--no-merges")
    since = config.get("since", "")
    until = config.get("until", "")
    log_options = config.get("log_options", "")

    # TODO: Make this user adjustable
    max_bar_length = 30

    if author:
        print(f"Git commits by weekday for author '{author}':")
    else:
        print("Git commits by weekday:")

    # Define the order of weekdays
    weekdays_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    # Initialize commit counts for each weekday
    commit_counts = {day: 0 for day in weekdays_order}

    # Original command:
    # git -c log.showSignature=false shortlog -n $_merges --format='%ad %s' \
    #     "${_author}" "$_since" "$_until" $_log_options |
    #     grep -cE "^ * $i \w\w\w [0-9]{1,2} " || continue
    author_option = f"--author={author}" if author else ""

    cmd = [
        "git",
        "-c",
        "log.showSignature=false",
        "log",
        merges,
        "--pretty=format:%cd",
        "--date=format:%a",
        author_option,
        since,
        until,
        log_options,
    ]

    # Remove any empty space from the cmd
    cmd = [arg for arg in cmd if arg]

    output = run_git_command(cmd)
    if output:
        # Split the output into individual weekday abbreviations
        weekdays = output.split("\n")
        for day in weekdays:
            if day in commit_counts:
                commit_counts[day] += 1

        # Calculate total commits
        total_commits = sum(commit_counts.values())
        if total_commits == 0:
            print("No commits found.")
            return

        # Determine the maximum count to set the scaling factor
        max_count = max(commit_counts.values())
        scaling_factor = (max_bar_length / max_count) if max_count > 0 else 0

        # Print the header row
        header_day = "Day"
        header_sum = "Sum"
        print(f"\t{header_day:<6}\t{header_sum:<4}")

        # Iterate through the weekdays in order and print counts with proper alignment
        for day in weekdays_order:
            count = commit_counts[day]
            if count > 0:
                # Calculate the number of blocks for the bar and make sure
                # there's at least one block for non-zero vals
                num_blocks = int(count * scaling_factor)
                if num_blocks == 0 and count > 0:
                    num_blocks = 1
                # Construct the bar with a leading "|"
                bar = "|" + "█" * num_blocks
            else:
                # Represent days with no commits with a dash
                bar = "-"

            # Print with alignment
            print(f"\t{day:<6}\t{count:<4}\t{bar}")
    else:
        if author:
            print(f"No commits found for author: {author}")
        else:
            print("No commits found.")


def git_commits_per_hour(config: Dict[str, Union[str, int]], author: Optional[str] = None) -> None:
    """
    Shows commits grouped by hour of the day. If an author is provided,
    it shows commits grouped by hour for that specific author.

    Args:
        config: Dict[str, Union[str, int]]: Config dictionary holding env vars.
        author (Optional[str]): The author to show the commits grouped by.
        If None, show for all authors.

    Returns:
        None
    """

    # Grab the config options from our config.py.
    # config.py should give fallbacks for these, but for sanity,
    # lets also provide some defaults just in case.
    merges = config.get("merges", "--no-merges")
    since = config.get("since", "")
    until = config.get("until", "")
    log_options = config.get("log_options", "")

    # TODO: Make this user adjustable
    max_bar_length = 20

    # Define the order of hours (00 to 23)
    hours_order = [f"{hour:02d}" for hour in range(24)]

    # Initialize commit counts for each hour
    commit_counts = {hour: 0 for hour in hours_order}

    if author:
        print(f"Git commits by hour for author '{author}':")
    else:
        print("Git commits by hour:")

    author_option = f"--author={author}" if author else ""

    # Original git command:
    #  git -c log.showSignature=false shortlog -n $_merges --format='%ad %s' \
    #      "${_author}" "$_since" "$_until" $_log_options |
    #      grep -cE '[0-9] '$i':[0-9]' || continue
    cmd = [
        "git",
        "-c",
        "log.showSignature=false",
        "log",
        merges,
        "--pretty=format:%cd",
        "--date=format:%H",
        author_option,
        since,
        until,
        log_options,
    ]

    # Remove any empty space from the cmd
    cmd = [arg for arg in cmd if arg]

    output = run_git_command(cmd)
    if output:
        # Split the output into individual hour abbreviations
        hours = output.split("\n")
        for hour in hours:
            if hour in commit_counts:
                commit_counts[hour] += 1

        # Calculate total commits
        total_commits = sum(commit_counts.values())
        if total_commits == 0:
            print("No commits found.")
            return

        # Determine the maximum count to set scaling
        max_count = max(commit_counts.values())
        scaling_factor = (max_bar_length / max_count) if max_count > 0 else 0

        # Print the header row
        header_hour = "Hour"
        header_sum = "Sum"
        print(f"\t{header_hour:<6}\t{header_sum:<4}")

        # Iterate through the hours in order and print counts with proper alignment
        for hour in hours_order:
            count = commit_counts[hour]
            if count > 0:
                # Calculate the number of blocks for the bar and make sure
                # there's at least one block for non-zero vals
                num_blocks = int(count * scaling_factor)
                if num_blocks == 0 and count > 0:
                    num_blocks = 1
                # Construct the bar with a leading "|"
                bar = "|" + "█" * num_blocks
            else:
                # Represent hours with no commits with a dash
                bar = "-"

            # Print with alignment
            print(f"\t{hour:<6}\t{count:<4}\t{bar}")
    else:
        if author:
            print(f"No commits found for author: {author}")
        else:
            print("No commits found.")


def git_commits_per_timezone(
    config: Dict[str, Union[str, int]], author: Optional[str] = None
) -> None:
    """
    Displays commits grouped by timezone. If an author is provided, it shows
    commits grouped by timezone for that specific author.

    Args:
        config: Dict[str, Union[str, int]]: Config dictionary holding env vars.
        author (Optional[str]): The author to show the commits grouped by.
        If None, show for all authors.

    Returns:
        None
    """

    # Grab the config options from our config.py.
    # config.py should give fallbacks for these, but for sanity,
    # lets also provide some defaults just in case.
    merges = config.get("merges", "--no-merges")
    since = config.get("since", "")
    until = config.get("until", "")
    log_options = config.get("log_options", "")
    pathspec = config.get("pathspec", "")

    # Initialize commit counts in a collection for easy storage and access
    commit_counts = collections.Counter()

    # Original command:
    #  git -c log.showSignature=false log $_merges --format='%ad %s' \
    #      "${_author}" "$_since" "$_until" --date=iso $_log_options $_pathspec \
    #      | cut -d " " -f 3 | grep -v -e '^[[:space:]]*$' | sort -n | uniq -c
    if author:
        print(f"Git commits by timezone for author '{author}':\n")
    else:
        print("Git commits by timezone:\n")

    author_option = f"--author={author}" if author else ""

    cmd = [
        "git",
        "-c",
        "log.showSignature=false",
        "log",
        merges,
        "--pretty=format:%ad %s",
        author_option,
        since,
        until,
        "--date=iso",
        log_options,
        pathspec,
    ]

    # Remove any empty space from the cmd
    cmd = [arg for arg in cmd if arg]

    output = run_git_command(cmd)
    if output:
        # Extract timezone offsets from each commit
        for line in output.split("\n"):
            parts = line.strip().split()
            if len(parts) >= 3:
                # ISO format: YYYY-MM-DD HH:MM:SS +/-TZ
                timezone = parts[2]
                # Validate timezone format (e.g., +0200, -0500)
                if (
                    timezone.startswith(("+", "-"))
                    and len(timezone) == 5
                    and timezone[1:].isdigit()
                ):
                    commit_counts[timezone] += 1

        if not commit_counts:
            if author:
                print(f"No valid timezones found for author: {author}")
            else:
                print("No valid timezones found in commits.")
            return

        # Calculate total commits
        total_commits = sum(commit_counts.values())
        if total_commits == 0:
            print("No commits found.")
            return

        # Print the header row
        header_commits = "Commits"
        header_timezone = "TimeZone"
        print(f"{header_commits:<7}\t{header_timezone:<8}")

        # Sort timezones by count descending and then by timezone
        sorted_timezones = sorted(commit_counts.items(), key=lambda x: (-x[1], x[0]))

        # Iterate through the sorted timezones and print counts
        for timezone, count in sorted_timezones:
            # TODO: Alignment slightly off of original
            print(f"{count:<7}\t{timezone:<8}")
    else:
        if author:
            print(f"No commits found for author: {author}")
        else:
            print("No commits found.")
