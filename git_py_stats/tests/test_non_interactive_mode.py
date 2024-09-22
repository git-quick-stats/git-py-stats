
from argparse import Namespace

import unittest
from unittest.mock import patch

from git_py_stats import non_interactive_mode, arg_parser


class TestNonInteractiveMode(unittest.TestCase):
    """
    Unit test class for testing the non_interactive_mode module
    """

    # Prevent output to stdout
    @patch('git_py_stats.generate_cmds.contribution_stats_by_author', return_value=None)
    @patch('git_py_stats.non_interactive_mode.print')
    def test_handle_non_interactive_mode(self, mock_print, mock_contribution_stats) -> None:
        """
        Test case for handle_non_interactive_mode in non_interactive_mode

        Simulates passing command-line arguments using the argument parser, and verifies
        that `handle_non_interactive_mode` executes without errors and returns `None`.

        The test uses `unittest.mock.patch` to mock `sys.argv` with a list of command-line arguments,
        the `contribution_stats_by_author` function to prevent actual execution, and the `print` function
        to prevent actual console output during testing.

        The function is expected to handle the namespace object without raising exceptions, call the
        `contribution_stats_by_author` function at least once if the corresponding argument is passed,
        and return `None`.
        """
        # Mock sys.argv to simulate command-line arguments
        test_args = ['git-py-stats', '--detailed-git-stats']

        # Use the argument parser to create an argument namespace
        with patch('sys.argv', test_args):
            args: Namespace = arg_parser.parse_arguments([])

        # Call the function and assert the result is None
        self.assertIsNone(non_interactive_mode.handle_non_interactive_mode(args))

        # Verify that the mocked function was called
        mock_contribution_stats.assert_called()

        # Verify that print was not called since the function should execute normally
        mock_print.assert_not_called()


if __name__ == '__main__':
    unittest.main()

