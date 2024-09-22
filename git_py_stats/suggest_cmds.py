"""
Functions related to the 'Suggest' section.
"""

from collections import Counter

from git_py_stats.git_operations import run_git_command


def code_reviewers() -> None:
    """
    Suggests potential code reviewers based on commit history.
    """
    cmd = ['git', 'log', '--format=%ae', '--no-merges']
    output = run_git_command(cmd)
    
    if output:
        emails = output.split('\n')
        counter = Counter(emails)
        reviewers = [email for email, count in counter.items()]
        
        if reviewers:
            print("Suggested code reviewers based on git history:")
            for reviewer in reviewers:
                print(reviewer)
        else:
            print('No potential reviewers found. Consider using a larger dataset.')
    else:
        print('No data available.')

