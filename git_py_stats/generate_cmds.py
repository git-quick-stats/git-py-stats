"""
Functions related to the 'Generate' section.
"""

import collections
import csv
import datetime
import json
import os
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
        first_commit = datetime.datetime.fromtimestamp(stats['first_commit']).strftime('%a %b %d %H:%M:%S %Y %z')
        last_commit = datetime.datetime.fromtimestamp(stats['last_commit']).strftime('%a %b %d %H:%M:%S %Y %z')

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



def git_changelogs_last_10_days(author: Optional[str] = None) -> None:
    """
    Shows commit messages from the last 10 days. If an author is provided, 
    it shows commit messages from that author.
    """

    if author:
        cmd = ['git', 'log', '--author', author, '--since=10.days', '--oneline']
    else:
        cmd = ['git', 'log', '--since=10.days', '--oneline']

    output = run_git_command(cmd)
    if output:
        if author:
            print(f"Git changelogs by {author} (last 10 days):")
        else:
            print("Git changelogs (last 10 days):")
        print(output)
    else:
        if author:
            print(f'No changelogs available for author {author} in the last 10 days.')
        else:
            print('No changelogs available in the last 10 days.')


def my_daily_status() -> None:
    """
    Displays the user's commits from the last day.
    """
    
    try:
        user = os.getlogin()
    except OSError:
        user = os.environ.get('USER', 'unknown')
    cmd = ['git', 'log', '--author', user, '--since=1.day', '--oneline']
    output = run_git_command(cmd)
    if output:
        print("My daily status:")
        print(output)
    else:
        print('No commits in the last day.')


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

