"""
Functions related to the 'Generate' section.
"""

import collections
import csv
import json
from typing import Optional, Dict, Any, List, Union, Tuple
from datetime import datetime, timedelta

from git_py_stats.git_operations import run_git_command


# TODO: This can also be part of the future detailed_git_stats refactor
def _author_sort_key(item: Tuple[str, Dict[str, Any]], sort_by: str) -> Tuple:
    """
    Helper function for detailed_git_stats to allow for easy sorting.

    Args:
        item: Tuple[str, Dict[str, Any]]: author_display_name and stats_dict
        sort_by (str): 'name', 'commits', 'insertions', 'deletions', or 'lines'

    Returns:
        A key suitable for sorting.
    """
    author, stats = item
    commits = int(stats.get("commits", 0) or 0)
    insertions = int(stats.get("insertions", 0) or 0)
    deletions = int(stats.get("deletions", 0) or 0)
    lines = int(stats.get("lines_changed", insertions + deletions) or 0)

    if sort_by == "commits":
        return (commits, author.lower())
    if sort_by == "insertions":
        return (insertions, author.lower())
    if sort_by == "deletions":
        return (deletions, author.lower())
    if sort_by == "lines":
        return (lines, author.lower())
    # default: name
    return (author.lower(),)


# TODO: We should really refactor this; It's huge
def detailed_git_stats(config: Dict[str, Union[str, int]], branch: Optional[str] = None) -> None:
    """
    Displays detailed contribution stats by author.

    Args:
        config: Dict[str, Union[str, int]]: Config dictionary holding env vars.
        branch (Optional[str]): Git branch to analyze. If None, use current branch.

    Returns:
        None
    """

    # Reset all relevant variables
    author_stats: Dict[str, Dict[str, Any]] = {}
    total_insertions = 0
    total_deletions = 0
    total_files = set()
    total_commits = 0

    # Variables to track current commit metadata
    current_author = ""
    current_date = 0

    # Grab the config options from our config.py.
    # config.py should give fallbacks for these, but for sanity,
    # lets also provide some defaults just in case.
    merges = config.get("merges", "--no-merges")
    since = config.get("since", "")
    until = config.get("until", "")
    log_options = config.get("log_options", "")
    pathspec = config.get("pathspec", "")

    # Original command:
    # git -c log.showSignature=false log ${_branch} --use-mailmap $_merges --numstat \
    #     --pretty="format:commit %H%nAuthor: %aN <%aE>%nDate:   %ad%n%n%w(0,4,4)%B%n" \
    #     "$_since" "$_until" $_log_options $_pathspec
    # Define the git base command
    cmd = [
        "git",
        "-c",
        "log.showSignature=false",
        "log",
    ]

    # Handle optional branch arg
    if branch:
        cmd.append(branch)

    # Create the rest of the command
    cmd.extend(
        [
            "--use-mailmap",
            merges,
            "--numstat",
            "--pretty=format:%H%x09%aN%x09%aE%x09%ad",
            "--date=raw",
            since,
            until,
            log_options,
            pathspec,
        ]
    )

    # Remove any empty space from the cmd
    cmd = [arg for arg in cmd if arg]

    output = run_git_command(cmd)
    if not output:
        return

    # Split the output into lines and process each line
    lines = output.split("\n")
    for line in lines:
        # Check if the line is empty or does not contain tab-separated values
        if line.strip() == "" or "\t" not in line:
            continue

        parts = line.split("\t")
        if len(parts) == 4:
            # Commit metadata
            commit_hash, author_name, author_email, date_raw = parts
            current_author = author_name
            current_date = int(date_raw.split()[0])

            # Initialize stats for the current author if not already done
            if author_name not in author_stats:
                author_stats[author_name] = {
                    "email": author_email,
                    "insertions": 0,
                    "deletions": 0,
                    "files": set(),
                    "commits": 0,
                    "lines_changed": 0,
                    "first_commit": current_date,
                    "last_commit": current_date,
                }
            # Increment commit count
            author_stats[author_name]["commits"] += 1
            total_commits += 1

            # Update first and last commit dates
            if current_date < author_stats[author_name]["first_commit"]:
                author_stats[author_name]["first_commit"] = current_date
            if current_date > author_stats[author_name]["last_commit"]:
                author_stats[author_name]["last_commit"] = current_date

        elif len(parts) == 3:
            # This line contains numstat data
            try:
                added, removed, filename = parts
                added = int(added) if added != "-" else 0
                removed = int(removed) if removed != "-" else 0

                if not current_author:
                    continue  # Skip if current_author is not set

                # Update stats for the current author
                author_stats[current_author]["insertions"] += added
                author_stats[current_author]["deletions"] += removed
                author_stats[current_author]["lines_changed"] += added + removed
                author_stats[current_author]["files"].add(filename)

                # Update total stats
                total_insertions += added
                total_deletions += removed
                total_files.add(filename)

            except ValueError:
                continue  # Skip lines that don't match expected format

    total_lines_changed = total_insertions + total_deletions
    total_files_changed = len(total_files)

    # Display the contribution stats for each author
    print(
        f"\n Contribution stats (by author) on the {'current' if not branch else branch} branch:\n"
    )

    # Sort authors by env-configured metric/direction
    sort_by = str(config.get("sort_by", "name")).lower()
    sort_dir = str(config.get("sort_dir", "asc")).lower()
    reverse = sort_dir == "desc"

    author_items = list(author_stats.items())
    author_items.sort(key=lambda it: _author_sort_key(it, sort_by), reverse=reverse)

    if author_items:
        print(f"\nSorting by: {sort_by} ({'desc' if reverse else 'asc'})\n")

    for author, stats in author_items:
        email = stats["email"]
        insertions = stats["insertions"]
        deletions = stats["deletions"]
        files = len(stats["files"])
        commits = stats["commits"]
        lines_changed = stats["lines_changed"]
        first_commit = datetime.fromtimestamp(stats["first_commit"]).strftime(
            "%a %b %d %H:%M:%S %Y %z"
        )
        last_commit = datetime.fromtimestamp(stats["last_commit"]).strftime(
            "%a %b %d %H:%M:%S %Y %z"
        )

        # Calculate percentages
        insertions_pct = (insertions / total_insertions * 100) if total_insertions else 0
        deletions_pct = (deletions / total_deletions * 100) if total_deletions else 0
        files_pct = (files / total_files_changed * 100) if total_files_changed else 0
        commits_pct = (commits / total_commits * 100) if total_commits else 0
        lines_changed_pct = (
            (lines_changed / total_lines_changed * 100) if total_lines_changed else 0
        )

        print(f"         {author} <{email}>:")
        print(f"          insertions:    {insertions:<6} ({insertions_pct:.0f}%)")
        print(f"          deletions:     {deletions:<6} ({deletions_pct:.0f}%)")
        print(f"          files:         {files:<6} ({files_pct:.0f}%)")
        print(f"          commits:       {commits:<6} ({commits_pct:.0f}%)")
        print(f"          lines changed: {lines_changed:<6} ({lines_changed_pct:.0f}%)")
        print(f"          first commit:  {first_commit}")
        print(f"          last commit:   {last_commit}\n")

    # Perform final calculation of stats
    print("         total:")
    print(f"           insertions:    {total_insertions:<6} (100%)")
    print(f"           deletions:     {total_deletions:<6} (100%)")
    print(f"           files:         {total_files_changed:<6} (100%)")
    print(f"           commits:       {total_commits:<6} (100%)\n")


def changelogs(config: Dict[str, Union[str, int]], author: Optional[str] = None) -> None:
    """
    Shows commit messages grouped by date for the last 'limit' dates
    where commits occurred.

    Args:
        config: Dict[str, Union[str, int]]: Config dictionary holding env vars.
        author: Optional[str]: If an author is provided, shows commit messages
        from that author. Otherwise, passes 'None' and shows commits from all authors.

    Returns:
        None
    """

    # Initialize variables similar to the Bash version
    next_date = datetime.now().date()
    author_option = f"--author={author}" if author else ""

    # Grab the config options from our config.py.
    # config.py should give fallbacks for these, but for sanity,
    # lets also provide some defaults just in case.
    merges = config.get("merges", "--no-merges")
    since = config.get("since", "")
    until = config.get("until", "")
    log_options = config.get("log_options", "")
    pathspec = config.get("pathspec", "")
    limit = int(config.get("limit", 10))

    # Original git command:
    # git -c log.showSignature=false log --use-mailmap $_merges --format="%cd"
    #     --date=short "${_author}" "$_since" "$_until" $_log_options $_pathspec
    cmd = [
        "git",
        "-c",
        "log.showSignature=false",
        "log",
        "--use-mailmap",
        merges,
        "--format=%cd",
        "--date=short",
    ]

    if author_option:
        cmd.append(author_option)

    cmd.extend([since, until, log_options, pathspec])

    # Remove any empty space from the cmd
    cmd = [arg for arg in cmd if arg]

    print(f"Git changelogs (last {limit} commits)")

    # Get commit dates
    output = run_git_command(cmd)
    if not output:
        print("No commits found.")
        return

    # Process dates by splitting into date strings,
    # removing dupes, sorting in reverse chrono order,
    # and applying our limit defined above
    dates = output.strip().split("\n")
    dates = sorted(set(dates), reverse=True)
    dates = dates[:limit]

    # Create the date/day format of [YYYY-MM-DD] - Day of week
    for date_str in dates:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        day_of_week = date.strftime("%A")

        print(f"\n[{date_str} - {day_of_week}]")

        since_date = (date - timedelta(days=1)).strftime("%Y-%m-%d")
        until_date = next_date.strftime("%Y-%m-%d")

        since_option = f"--since={since_date}"
        until_option = f"--until={until_date}"

        # Build git log command for the date range
        # Note the space between the --format and *. This provides
        # the space should there be multiple entries per date string
        # Original version:
        #  git -c log.showSignature=false log \
        #      --use-mailmap $_merges --format=" * %s (%aN)" \
        #      "${_author}" --since==$(date -d "$DATE - 1 day" +"%Y-%m-%d") \
        #      --until=$next
        date_cmd = [
            "git",
            "-c",
            "log.showSignature=false",
            "log",
            "--use-mailmap",
            merges,
            "--format= * %s (%aN)",
        ]

        if author_option:
            date_cmd.append(author_option)

        date_cmd.extend([since_option, until_option])

        # Remove any empty space from the date_cmd
        date_cmd = [arg for arg in date_cmd if arg]
        # Output everything to the terminal
        # Note the space added. This provides the initial space
        # before the asterisk for every initial entry
        output = run_git_command(date_cmd)
        if output:
            print(f" {output}")
        next_date = date  # Update next_date for the next iteration


def my_daily_status(config: Dict[str, Union[str, int]]) -> None:
    """
    Displays the user's commits from the last day.

    Args:
        config: Dict[str, Union[str, int]]: Config dictionary holding env vars.

    Returns:
        None
    """
    # Grab the config options from our config.py.
    # config.py should give fallbacks for these, but for sanity,
    # lets also provide some defaults just in case.
    merges = config.get("merges", "--no-merges")
    log_options = config.get("log_options", "")

    print("My daily status:")
    # Equivalent Bash Command:
    # git diff --shortstat '@{0 day ago}' | sort -nr | tr ',' '\n' \
    #     | LC_ALL=C awk '{ args[NR] = $0; } END { for (i = 1; i <= NR; ++i) \
    #                     { printf "\t%s\n", args[i] } }'

    # Mimic 'git diff --shortstat "@{0 day ago}"'
    diff_cmd = ["git", "diff", "--shortstat", "@{0 day ago}"]
    diff_output = run_git_command(diff_cmd)
    if diff_output:
        # Replace commas with newlines
        diff_lines = [line.strip() for line in diff_output.split(",")]
        # Print each line prefixed with a tab
        for line in diff_lines:
            print(f"\t{line}")
    else:
        # If no diff stats are available, indicate no changes
        print("\tNo changes in the last day.")

    # Count Commits
    # Equivalent Bash Command:
    # git -c log.showSignature=false log --use-mailmap \
    #     --author="$(git config user.name)" $_merges \
    #     --since=$(date "+%Y-%m-%dT00:00:00") \
    #     --until=$(date "+%Y-%m-%dT23:59:59") --reverse $_log_options \
    #     | grep -cE "commit [a-f0-9]{40}"

    # Get the user's name
    # Lets also handle the case if the user's name is not set correctly

    git_user = run_git_command(["git", "config", "user.name"])
    if not git_user:
        git_user = "unknown"

    # Get today's date in the format 'YYYY-MM-DD' to match the original cmd
    today = datetime.now().strftime("%Y-%m-%d")
    since = f"--since={today}T00:00:00"
    until = f"--until={today}T23:59:59"

    # Build the final git log command
    log_cmd = [
        "git",
        "-c",
        "log.showSignature=false",
        "log",
        "--use-mailmap",
        f"--author={git_user}",  # Ensure the 'f' prefix is present
        merges,
        since,
        until,
        "--reverse",
        "--pretty=%H",  # Output only commit hashes
        log_options,
    ]

    # Remove any empty space from the log_cmd
    log_cmd = [arg for arg in log_cmd if arg]
    # Execute the git log command
    log_output = run_git_command(log_cmd)

    # Bash version uses grep to count lines matching the hash pattern
    # "commit [a-f0-9]{40}". But it's not necessary with %H.
    # TODO: We are be able to do --pretty=format:%H to avoid
    #       having to use a regex to handle this portion.
    #       Feed back to the original project
    if log_output:
        commit_count = len(log_output.strip().splitlines())
    else:
        commit_count = 0
    # Print the commit count, prefixed with a tab
    print(f"\t{commit_count} commits")


def output_daily_stats_csv(config: Dict[str, Union[str, int]]) -> None:
    """
    Exports daily commit counts to a CSV file.

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
    branch = config.get("branch", "")
    ignore_authors = config.get("ignore_authors", lambda _s: False)

    if not branch:
        branch = input("Enter branch name (leave empty for current branch): ")

    # Original command:
    # git -c log.showSignature=false log ${_branch} --use-mailmap $_merges --numstat \
    #     --pretty="format:commit %H%nAuthor: %aN <%aE>%nDate:   %ad%n%n%w(0,4,4)%B%n" \
    #     "$_since" "$_until" $_log_options $_pathspec
    cmd = [
        "git",
        "-c",
        "log.showSignature=false",
        "log",
        branch,
        "--use-mailmap",
        merges,
        "--numstat",
        "--pretty=format:commit %H%nAuthor: %aN <%aE>%nDate:   %ad%n%n%w(0,4,4)%B%n",
        since,
        until,
        log_options,
        pathspec,
    ]

    # Remove any empty space from the cmd
    cmd = [arg for arg in cmd if arg]

    output = run_git_command(cmd)

    # Exit early if no output valid
    if not output:
        print("No data available.")
        return

    # NOTE: This has to be expanded to handle the new ability to ignore
    # authors, but there might be a better way to handle this...
    kept_lines = []
    current_block = []
    current_ignored = False
    have_seen_author = False

    for line in output.splitlines():
        # New commit starts
        if line.startswith("commit "):
            # Flush the previous block
            if current_block and not current_ignored:
                kept_lines.extend(current_block)
            # Reset for the next block
            current_block = [line]
            current_ignored = False
            have_seen_author = False
            continue

        # Only check author once per block
        if not have_seen_author and line.startswith("Author: "):
            author_line = line[len("Author: ") :].strip()
            name = author_line
            email = ""
            if "<" in author_line and ">" in author_line:
                name = author_line.split("<", 1)[0].strip()
                email = author_line.split("<", 1)[1].split(">", 1)[0].strip()

            # If any form matches (name or email), drop the whole block
            if (
                ignore_authors(author_line)
                or ignore_authors(name)
                or (email and ignore_authors(email))
            ):
                current_ignored = True
            have_seen_author = True
        current_block.append(line)

    # Flush the last block
    if current_block and not current_ignored:
        kept_lines.extend(current_block)

    # Found nothing worth keeping? Just exit then
    if not kept_lines:
        print("No data available.")
        return

    counter = collections.Counter(kept_lines)
    filename = "git_daily_stats.csv"
    try:
        with open(filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["Date", "Commits"])
            writer.writeheader()
            for text, count in sorted(counter.items()):
                writer.writerow({"Date": text, "Commits": count})
        print(f"Daily stats saved to {filename}")
    except IOError as e:
        print(f"Failed to write to {filename}: {e}")


# TODO: This doesn't match the original functionality as it uses some pretty
#       tricky shell code to format everything, as well as blast a bunch of
#       info out into a JSON file. For now, let's take a simple approach
#       that'll meet the needs of most people
def save_git_log_output_json(config: Dict[str, Union[str, int]]) -> None:
    """
    Saves detailed commit logs to a JSON file.

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

    # Original command:
    # git -c log.showSignature=false log --use-mailmap $_merges \
    #     "$_since" "$_until" $_log_options \
    #     --pretty=format: <trimmed for brevity>
    cmd = [
        "git",
        "-c",
        "log.showSignature=false",
        "log",
        "--use-mailmap",
        merges,
        since,
        until,
        log_options,
        "--pretty=format:%H|%aN|%ad|%s",
        "--date=iso",
    ]

    # Remove any empty space from the cmd
    cmd = [arg for arg in cmd if arg]

    # Process the output into a JSON file
    output = run_git_command(cmd)
    if output:
        commits: List[Dict[str, Any]] = []
        for line in output.split("\n"):
            try:
                commit_hash, author, date, message = line.split("|", 3)
                commits.append(
                    {
                        "hash": commit_hash,
                        "author": author,
                        "date": date,
                        "message": message,
                    }
                )
            except ValueError:
                continue  # Skip lines that don't match the expected format
        filename = "git_log.json"
        try:
            with open(filename, "w") as jsonfile:
                json.dump(commits, jsonfile, indent=4)
            print(f"Git log saved to {filename}")
        except IOError as e:
            print(f"Failed to write to {filename}: {e}")
    else:
        print("No log data available.")
