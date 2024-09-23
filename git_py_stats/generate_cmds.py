"""
Functions related to the 'Generate' section.
"""

import collections
import csv
from datetime import datetime, timedelta
import json
import os
import re
from typing import Optional, Dict, Any, List
from git_py_stats.git_operations import run_git_command


def contribution_stats_by_author(branch: Optional[str] = None) -> None:
    """
    Displays detailed contribution stats by author.

    Args:
        branch: The git branch to analyze. If None, use the current branch.
    """

    # NOTE: This is fairly annotated since the original function
    #       is fairly complex in general, and I wanted this to be
    #       as close as possible.

    # Reset all relevant variables
    author_stats: Dict[str, Dict[str, Any]] = {}
    total_insertions = 0
    total_deletions = 0
    total_files = set()
    total_commits = 0

    # Define the git command
    cmd = [
        'git', 'log',
        '--pretty=format:%H%x09%an%x09%ae%x09%ad',
        '--numstat',
        '--date=raw'
    ]
    if branch:
        cmd.append(branch)

    output = run_git_command(cmd)
    if not output:
        return

    # Variables to track current commit metadata
    current_author = ''
    current_email = ''
    current_date = 0

    # Split the output into lines and process each line
    lines = output.split('\n')
    for line in lines:
        # Check if the line is empty or does not contain tab-separated values
        if line.strip() == '' or '\t' not in line:
            continue

        parts = line.split('\t')
        if len(parts) == 4:
            # Commit metadata
            commit_hash, author_name, author_email, date_raw = parts
            current_author = author_name
            current_email = author_email
            current_date = int(date_raw.split()[0])

            # Initialize stats for the current author if not already done
            if author_name not in author_stats:
                author_stats[author_name] = {
                    'email': author_email,
                    'insertions': 0,
                    'deletions': 0,
                    'files': set(),
                    'commits': 0,
                    'lines_changed': 0,
                    'first_commit': current_date,
                    'last_commit': current_date
                }
            # Increment commit count
            author_stats[author_name]['commits'] += 1
            total_commits += 1

            # Update first and last commit dates
            if current_date < author_stats[author_name]['first_commit']:
                author_stats[author_name]['first_commit'] = current_date
            if current_date > author_stats[author_name]['last_commit']:
                author_stats[author_name]['last_commit'] = current_date

        elif len(parts) == 3:
            # This line contains numstat data
            try:
                added, removed, filename = parts
                added = int(added) if added != '-' else 0
                removed = int(removed) if removed != '-' else 0

                if not current_author:
                    continue  # Skip if current_author is not set

                # Update stats for the current author
                author_stats[current_author]['insertions'] += added
                author_stats[current_author]['deletions'] += removed
                author_stats[current_author]['lines_changed'] += added + removed
                author_stats[current_author]['files'].add(filename)

                # Update total stats
                total_insertions += added
                total_deletions += removed
                total_files.add(filename)

            except ValueError:
                continue  # Skip lines that don't match expected format

    total_lines_changed = total_insertions + total_deletions
    total_files_changed = len(total_files)

    # Display the contribution stats for each author
    print(f"\n Contribution stats (by author) on the {'current' if not branch else branch} branch:\n")

    # Sort authors alphabetically
    sorted_authors = sorted(author_stats.items(), key=lambda x: x[0])

    for author, stats in sorted_authors:
        email = stats['email']
        insertions = stats['insertions']
        deletions = stats['deletions']
        files = len(stats['files'])
        commits = stats['commits']
        lines_changed = stats['lines_changed']
        first_commit = datetime.fromtimestamp(stats['first_commit']).strftime('%a %b %d %H:%M:%S %Y %z')
        last_commit = datetime.fromtimestamp(stats['last_commit']).strftime('%a %b %d %H:%M:%S %Y %z')

        # Calculate percentages
        insertions_pct = (insertions / total_insertions * 100) if total_insertions else 0
        deletions_pct = (deletions / total_deletions * 100) if total_deletions else 0
        files_pct = (files / total_files_changed * 100) if total_files_changed else 0
        commits_pct = (commits / total_commits * 100) if total_commits else 0
        lines_changed_pct = (lines_changed / total_lines_changed * 100) if total_lines_changed else 0

        print(f"         {author} <{email}>:")
        print(f"          insertions:    {insertions:<6} ({insertions_pct:.0f}%)")
        print(f"          deletions:     {deletions:<6} ({deletions_pct:.0f}%)")
        print(f"          files:         {files:<6} ({files_pct:.0f}%)")
        print(f"          commits:       {commits:<6} ({commits_pct:.0f}%)")
        print(f"          lines changed: {lines_changed:<6} ({lines_changed_pct:.0f}%)")
        print(f"          first commit:  {first_commit}")
        print(f"          last commit:   {last_commit}\n")

    # Perform final calculation of stats
    print(f"         total:")
    print(f"           insertions:    {total_insertions:<6} (100%)")
    print(f"           deletions:     {total_deletions:<6} (100%)")
    print(f"           files:         {total_files_changed:<6} (100%)")
    print(f"           commits:       {total_commits:<6} (100%)\n")


def changelogs(author: Optional[str] = None, limit: int = 10) -> None:
    """
    Shows commit messages grouped by date, for the last 'limit' dates where commits occurred.

    Args:
        If an author is provided, it shows commit messages from that author.
        Otherwise, it passes 'None' and shows commits from all authors.
    """

    # Initialize variables similar to the Bash version
    # TODO: Refactor this when we add global adjustment capabilities
    next_date = datetime.now().date()
    author_option = f'--author={author}' if author else ''
    merges_option = '--no-merges'  # Adjust as per the Bash global variable _merges

    # Get unique commit dates
    # Original version:
    # git -c log.showSignature=false log --use-mailmap $_merges --format="%cd" --date=short "${_author}"
    #     "$_since" "$_until" $_log_options $_pathspec
    cmd = ['git', 'log', '--use-mailmap', merges_option, '--format=%cd', '--date=short']
    if author_option:
        cmd.append(author_option)

    print('Git changelogs (last 10 commits)')

    # Get commit dates
    output = run_git_command(cmd)
    if not output:
        print("No commits found.")
        return

    # Process dates by splitting into date strings,
    # removing dupes, sorting in reverse chrono order,
    # and applying our limit defined above
    dates = output.strip().split('\n')
    dates = sorted(set(dates), reverse=True)
    dates = dates[:limit]

    # Create the date/day format of [YYYY-MM-DD] - Day of week
    for date_str in dates:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        day_of_week = date.strftime('%A')
        print(f"\n[{date_str} - {day_of_week}]")

        since_date = (date - timedelta(days=1)).strftime('%Y-%m-%d')
        until_date = next_date.strftime('%Y-%m-%d')

        # Build git log command for the date range
        # Note the space between the --format and *. This provides
        # the space should there be multiple entries per date string
        # Original version:
        #  git -c log.showSignature=false log \
        #      --use-mailmap $_merges --format=" * %s (%aN)" \
        #      "${_author}" --since==$(date -d "$DATE - 1 day" +"%Y-%m-%d") \
        #      --until=$next
        cmd = [
            'git', 'log', '--use-mailmap', merges_option,
            '--format= * %s (%aN)',
            f'--since={since_date}',
            f'--until={until_date}'
        ]
        if author_option:
            cmd.append(author_option)

        # Output everything to the terminal
        # Note the space added. This provides the initial space
        # before the asterisk for every initial entry
        output = run_git_command(cmd)
        if output:
            print(f" {output}")
        next_date = date  # Update next_date for the next iteration


def my_daily_status() -> None:
    """
    Displays the user's commits from the last day.
    """

    print('My daily status:')

    # Equivalent Bash Command:
    # git diff --shortstat '@{0 day ago}' | sort -nr | tr ',' '\n' \
    #     | LC_ALL=C awk '{ args[NR] = $0; } END { for (i = 1; i <= NR; ++i) \
    #                     { printf "\t%s\n", args[i] } }'

    # Mimic 'git diff --shortstat "@{0 day ago}"'
    diff_cmd = ['git', 'diff', '--shortstat', '@{0 day ago}']
    diff_output = run_git_command(diff_cmd)

    # Process diff output:
    if diff_output:
        # Replace commas with newlines
        diff_lines = [line.strip() for line in diff_output.split(',')]

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
    git_user = run_git_command(['git', 'config', 'user.name'])
    if not git_user:
        git_user = 'unknown'

    # Define global variables with default values
    # TODO: Refactor these to be configurable
    merges_option = '--no-merges'
    log_options = ''

    # Get today's date in the format 'YYYY-MM-DD' to match the original cmd
    today = datetime.now().strftime('%Y-%m-%d')
    since = f"{today}T00:00:00"
    until = f"{today}T23:59:59"

    # Build the final git log command
    log_cmd = [
        'git', '-c', 'log.showSignature=false', 'log',
        '--use-mailmap',
        '--author', git_user,
        merges_option,
        '--since', since,
        '--until', until,
        '--reverse'
    ]

    # Added to handle log options in the future
    if log_options:
        log_cmd.extend(log_options.split())

    # Execute the git log command
    log_output = run_git_command(log_cmd)

    # Bash version uses grep to count lines matching the hash pattern
    # "commit [a-f0-9]{40}"
    # We can use re to mimic this in Python
    # TODO: Revisit this. We might be able to do --pretty=format:%H to avoid
    #       having to use a regex to handle this portion. This could be
    #       an improvement to feed back to the original project
    if log_output:
        commit_pattern = re.compile(r'^commit [a-f0-9]{40}$', re.MULTILINE)
        commit_count = len(commit_pattern.findall(log_output))
    else:
        commit_count = 0

    # Print the commit count, prefixed with a tab
    print(f"\t{commit_count} commits")


def output_daily_stats_csv() -> None:
    """
    Exports daily commit counts to a CSV file.
    """
    
    branch = input("Enter branch name (leave empty for current branch): ")
    cmd = ['git', 'log', '--date=short', '--pretty=format:%cd']
    if branch:
        cmd.insert(2, branch)
    output = run_git_command(cmd)
    if output:
        dates = output.split('\n')
        counter = collections.Counter(dates)
        filename = 'daily_stats.csv'
        try:
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['Date', 'Commits']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for date, count in sorted(counter.items()):
                    writer.writerow({'Date': date, 'Commits': count})
            print(f"Daily stats saved to {filename}")
        except IOError as e:
            print(f"Failed to write to {filename}: {e}")
    else:
        print('No data available.')


# TODO: This doesn't match the original functionality
def save_git_log_output_json() -> None:
    """
    Saves detailed commit logs to a JSON file.
    """
    
    cmd = ['git', 'log', '--pretty=format:%H|%an|%ad|%s', '--date=iso']
    output = run_git_command(cmd)
    if output:
        commits: List[Dict[str, Any]] = []
        for line in output.split('\n'):
            try:
                commit_hash, author, date, message = line.split('|', 3)
                commits.append({
                    'hash': commit_hash,
                    'author': author,
                    'date': date,
                    'message': message
                })
            except ValueError:
                continue  # Skip lines that don't match the expected format
        filename = 'git_log.json'
        try:
            with open(filename, 'w') as jsonfile:
                json.dump(commits, jsonfile, indent=4)
            print(f"Git log saved to {filename}")
        except IOError as e:
            print(f"Failed to write to {filename}: {e}")
    else:
        print('No log data available.')

