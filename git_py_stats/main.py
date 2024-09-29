#!/usr/bin/env python3

"""
Main entry point for Git Py Stats.
"""

import sys

from git_py_stats.git_operations import check_git_repository
from git_py_stats.arg_parser import parse_arguments
from git_py_stats.interactive_mode import handle_interactive_mode
from git_py_stats.non_interactive_mode import handle_non_interactive_mode
from git_py_stats.config import get_config


def main() -> None:
    """
    Main function that handles both interactive and non-interactive modes.

    Args:
        None

    Returns:
        None
    """

    # Check if we are inside a Git repository
    if not check_git_repository():
        print("This is not a git repository.")
        print("Please navigate to a git repository and try again.")
        sys.exit(1)

    # Get env config
    config = get_config()

    # Parse command-line arguments
    args = parse_arguments()

    # Non-Interactive Mode based on if we see command-line arguments
    if len(sys.argv) > 1:
        handle_non_interactive_mode(args, config)
    else:
        handle_interactive_mode(config)


if __name__ == "__main__":
    main()
