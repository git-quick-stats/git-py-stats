"""
Provides CLI parsing for Git Py Stats.
"""

# TODO: list is not subscriptable before Python 3.9, so we need to work
#       around this. However, Python 3.8 EOLs in October 2024. Let's keep
#       using older Python 3 ways of doing this, but mark this as a future
#       refactor...whenever I decide to upgrade my own version of Python.
from argparse import ArgumentParser, Namespace
from typing import List, Optional


def parse_arguments(argv: Optional[List[str]] = None) -> Namespace:
    """
    Parse command-line arguments and return them.

    Args:
        argv (Optional[List[str]]): List of arguments to parse (default: None).

    Returns:
        Namespace: Parsed command-line arguments as a Namespace object.

    Example:
        args = parse_arguments(['--detailed-git-stats'])
        print(args.detailed_git_stats)  # True
    """

    parser = ArgumentParser(
        description="Git Py Stats - A Python Implementation of Git Quick Stats.",
        allow_abbrev=False,  # Force users to be explicit. Makes testing sane.
    )

    # Generate Options
    parser.add_argument(
        "-T",
        "--detailed-git-stats",
        action="store_true",
        help="Give a detailed list of git stats",
    )
    parser.add_argument(
        "-R",
        "--git-stats-by-branch",
        metavar="BRANCH",
        type=str,
        help="See detailed list of git stats by branch",
    )
    parser.add_argument(
        "-c",
        "--changelogs",
        action="store_true",
        help="See changelogs",
    )
    parser.add_argument(
        "-L",
        "--changelogs-by-author",
        metavar='"AUTHOR NAME"',
        type=str,
        help="See changelogs by author",
    )
    parser.add_argument(
        "-S",
        "--my-daily-stats",
        action="store_true",
        help="See your current daily stats",
    )
    parser.add_argument(
        "-V",
        "--csv-output-by-branch",
        action="store_true",
        help="Output daily stats by branch in CSV format",
    )
    parser.add_argument(
        "-j",
        "--json-output",
        action="store_true",
        help="Save git log as a JSON formatted file to a specified area",
    )

    # List Options
    parser.add_argument(
        "-b",
        "--branch-tree",
        action="store_true",
        help="Show an ASCII graph of the git repo branch history",
    )
    parser.add_argument(
        "-D",
        "--branches-by-date",
        action="store_true",
        help="Show branches by date",
    )
    parser.add_argument(
        "-C",
        "--contributors",
        action="store_true",
        help="See a list of everyone who contributed to the repo",
    )
    parser.add_argument(
        "-n",
        "--new-contributors",
        metavar="DATE",
        type=str,
        help="List everyone who made their first contribution since a specified date",
    )
    parser.add_argument(
        "-a",
        "--commits-per-author",
        action="store_true",
        help="Displays a list of commits per author",
    )
    parser.add_argument(
        "-d",
        "--commits-per-day",
        action="store_true",
        help="Displays a list of commits per day",
    )
    parser.add_argument(
        "-Y",
        "--commits-by-year",
        action="store_true",
        help="Displays a list of commits per year",
    )
    parser.add_argument(
        "-m",
        "--commits-by-month",
        action="store_true",
        help="Displays a list of commits per month",
    )
    parser.add_argument(
        "-w",
        "--commits-by-weekday",
        action="store_true",
        help="Displays a list of commits per weekday",
    )
    parser.add_argument(
        "-W",
        "--commits-by-author-by-weekday",
        metavar='"AUTHOR NAME"',
        type=str,
        help="Displays a list of commits per weekday by author",
    )
    parser.add_argument(
        "-o",
        "--commits-by-hour",
        action="store_true",
        help="Displays a list of commits per hour",
    )
    parser.add_argument(
        "-A",
        "--commits-by-author-by-hour",
        metavar='"AUTHOR NAME"',
        type=str,
        help="Displays a list of commits per hour by author",
    )
    parser.add_argument(
        "-z",
        "--commits-by-timezone",
        action="store_true",
        help="Displays a list of commits per timezone",
    )
    parser.add_argument(
        "-Z",
        "--commits-by-author-by-timezone",
        metavar='"AUTHOR NAME"',
        type=str,
        help="Displays a list of commits per timezone by author",
    )

    # Calendar Options
    parser.add_argument(
        "-k",
        "--commits-calendar-by-author",
        metavar='"AUTHOR NAME"',
        type=str,
        help="Show a calendar of commits by author",
    )

    parser.add_argument(
        "-H",
        "--commits-heatmap",
        action="store_true",
        help="Show a heatmap of commits per day-of-week",
    )

    # Suggest Options
    parser.add_argument(
        "-r",
        "--suggest-reviewers",
        action="store_true",
        help="Show the best people to contact to review code",
    )

    # Help option inherited from argparse by default, no need to impl them.

    return parser.parse_args(argv)
