"""
Functions related to the 'List' section.
"""

import collections
import datetime
from typing import Dict, Optional

from git_py_stats.git_operations import run_git_command


def branch_tree_view() -> None:
    """
    Displays a visual graph of recent commits across all branches.
    """
    
    cmd = ['git', 'log', '--graph', '--oneline', '--all', '-n', '10']
    output = run_git_command(cmd)
    if output:
        print("Branch tree view (last 10 commits):")
        print(output)
    else:
        print('No data available.')


def all_branches_sorted() -> None:
    """
    Lists branches sorted by the latest commit date.
    """
    
    cmd = [
        'git', 'for-each-ref', '--sort=-committerdate', '--format', '%(refname:short)',
        'refs/heads/'
    ]
    output = run_git_command(cmd)
    if output:
        print("All branches sorted by most recent commits:")
        print(output)
    else:
        print('No branches available.')


def all_contributors() -> None:
    """
    Lists all contributors alphabetically.
    """
    
    cmd = ['git', 'shortlog', '-sn', '--all']
    output = run_git_command(cmd)
    if output:
        print("All contributors:")
        contributors = [line.strip() for line in output.split('\n')]
        contributors.sort(key=lambda x: x.split('\t')[1])
        for contributor in contributors:
            print(contributor)
    else:
        print('No contributors found.')


def new_contributors() -> None:
    """
    Lists contributors sorted by email.
    """
    
    cmd = ['git', 'log', '--format=%aN|%aE']
    output = run_git_command(cmd)
    if output:
        contributors = set(output.split('\n'))
        new_contributors_list = sorted(contributors, key=lambda x: x.split('|')[1])
        print("New contributors:")
        for contributor in new_contributors_list:
            try:
                name, email = contributor.split('|')
                print(f"{name} <{email}>")
            except ValueError:
                continue  # Skip lines that don't match the expected format
    else:
        print('No contributors found.')


def git_commits_per_author() -> None:
    """
    Shows the number of commits per author.
    """
    
    cmd = ['git', 'shortlog', '-s', '-n']
    output = run_git_command(cmd)
    if output:
        print("Git commits per author:")
        print(output)
    else:
        print('No commits found.')


def git_commits_per_date() -> None:
    """
    Displays commits grouped by date.
    """
    
    cmd = ['git', 'log', '--date=short', '--pretty=format:%cd']
    output = run_git_command(cmd)
    if output:
        dates = output.split('\n')
        counter = collections.Counter(dates)
        print("Git commits per date:")
        for date, count in sorted(counter.items()):
            print(f"{date}: {count} commits")
    else:
        print('No commits found.')


def git_commits_per_month() -> None:
    """
    Displays commits grouped by month.
    """
    
    cmd = ['git', 'log', '--date=format:%Y-%m', '--pretty=format:%cd']
    output = run_git_command(cmd)
    if output:
        months = output.split('\n')
        counter = collections.Counter(months)
        print("Git commits per month:")
        for month, count in sorted(counter.items()):
            print(f"{month}: {count} commits")
    else:
        print('No commits found.')


def git_commits_per_year() -> None:
    """
    Displays commits grouped by year.
    """
    
    cmd = ['git', 'log', '--date=format:%Y', '--pretty=format:%cd']
    output = run_git_command(cmd)
    if output:
        years = output.split('\n')
        counter = collections.Counter(years)
        print("Git commits per year:")
        for year, count in sorted(counter.items()):
            print(f"{year}: {count} commits")
    else:
        print('No commits found.')


def git_commits_per_weekday(author: Optional[str] = None) -> None:
    """
    Shows commits grouped by weekday. If an author is provided, it shows
    commits grouped by weekday for that specific author.

    Args:
        author (Optional[str]): The author you want to show the commits grouped by.
                                If None, show for all authors.
    """
    
    # Build git cmd based on whether or not we have an author provided
    if author:
        cmd = ['git', 'log', '--author', author, '--pretty=format:%cd', '--date=raw']
    else:
        cmd = ['git', 'log', '--pretty=format:%cd', '--date=raw']

    # Run the git command and capture the output
    output = run_git_command(cmd)

    if output:
        try:
            timestamps = [int(line.split()[0]) for line in output.split('\n')]
            weekdays = [datetime.datetime.fromtimestamp(ts).strftime('%A') for ts in timestamps]
            counter = collections.Counter(weekdays)

            # Display commits per weekday
            if author:
                print(f"Git commits per weekday for author '{author}':")
            else:
                print("Git commits per weekday:")

            for day, count in counter.most_common():
                print(f"  {day}: {count} commits")

        except (ValueError, IndexError):
            print("Failed to parse timestamps.")
    else:
        if author:
            print(f'No commits found for author: {author}')
        else:
            print('No commits found.')


def git_commits_per_hour(author: Optional[str] = None) -> None:
    """
    Shows commits grouped by hour of the day. If an author is provided, 
    it shows commits grouped by hour for that specific author.

    Args:
        author (Optional[str]): The author to show the commits grouped by. 
                                If None, show for all authors.
    """
    
    # Build git cmd based on whether or not we have an author provided
    if author:
        cmd = ['git', 'log', '--author', author, '--pretty=format:%cd', '--date=raw']
    else:
        cmd = ['git', 'log', '--pretty=format:%cd', '--date=raw']

    # Run the git command and capture the output
    output = run_git_command(cmd)

    if output:
        try:
            timestamps = [int(line.split()[0]) for line in output.split('\n')]
            hours = [datetime.datetime.fromtimestamp(ts).hour for ts in timestamps]
            counter = collections.Counter(hours)

            # Display commits per hour
            if author:
                print(f"Git commits per hour for author '{author}':")
            else:
                print("Git commits per hour:")

            for hour, count in sorted(counter.items()):
                print(f"  {hour:02d}:00 - {count} commits")

        except (ValueError, IndexError):
            print("Failed to parse timestamps.")
    else:
        if author:
            print(f'No commits found for author: {author}')
        else:
            print('No commits found.')


def git_commits_per_timezone(author: Optional[str] = None) -> None:
    """
    Displays commits grouped by timezone. If an author is provided, it shows
    commits grouped by timezone for that specific author.

    Args:
        author (Optional[str]): The author to show the commits grouped by.
                                If None, show for all authors.
    """
    
    # Build git cmd based on whether or not we have an author provided
    if author:
        cmd = ['git', 'log', '--author', author, '--pretty=format:%cd', '--date=raw']
    else:
        cmd = ['git', 'log', '--pretty=format:%cd', '--date=raw']

    # Run the git command and capture the output
    output = run_git_command(cmd)

    if output:
        try:
            timezones = []
            for line in output.split('\n'):
                parts = line.split()
                if len(parts) == 2:  # Check if we have the format: "timestamp timezone"
                    _, timezone = parts
                    # Check if the second part is a valid timezone offset
                    if timezone.startswith(('+', '-')):
                        timezones.append(timezone)

            if timezones:
                counter = collections.Counter(timezones)
                if author:
                    print(f"Git commits per timezone for author '{author}':")
                else:
                    print("Git commits per timezone:")
                
                for tz, count in counter.most_common():
                    print(f"  {tz}: {count} commits")
            else:
                if author:
                    print(f"No valid timezones found for author: {author}")
                else:
                    print("No valid timezones found in commits.")
                    
        except IndexError:
            print("Failed to parse timezones.")
    else:
        if author:
            print(f'No commits found for author: {author}')
        else:
            print('No commits found.')
