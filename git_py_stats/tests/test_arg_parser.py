import io
import sys
from argparse import Namespace

import unittest
from unittest.mock import patch, MagicMock

from git_py_stats import arg_parser


class TestArgParser(unittest.TestCase):
    """
    Unit test class for testing the argument parser functionality.
    """

    # Arg parser needs to mock stdout and stderr
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_parse_arguments(self, mock_stderr, mock_stdout) -> None:
        """
        Test case for parse_arguments in arg_parser.

        This test simulates passing the '--help' command-line argument to the argument parser
        and verifies that the parser exits with a SystemExit code of 0, indicating successful
        parsing and help message display.

        The `sys.argv` is mocked with a list of command-line arguments to simulate different
        command-line inputs. The test checks for the SystemExit exception, which is raised by
        argparse when displaying help.

        The test also mocks `sys.stdout` and `sys.stderr` to prevent output to the terminal and
        capture the help message for verification.
        """

        # Mock sys.argv with expected command-line arguments
        test_args = ['git-py-stats', '--help']

        # Patch sys.argv with test_args
        with patch('sys.argv', test_args):
            # Expect SystemExit when '--help' is passed
            with self.assertRaises(SystemExit) as cm:
                # Call parse_arguments with an empty list to simulate no additional args
                args: Namespace = arg_parser.parse_arguments([])

            # Check that SystemExit was called with code 0
            self.assertEqual(cm.exception.code, 0)

        # Verify that the help message was printed to stdout
        output = mock_stdout.getvalue()
        self.assertIn("usage:", output)
        self.assertIn("Git Py Stats - A Python Implementation of Git Quick Stats.", output)

if __name__ == '__main__':
    unittest.main()

