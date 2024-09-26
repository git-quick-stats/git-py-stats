import unittest
from unittest.mock import patch, MagicMock
from git_py_stats import generate_cmds
from git_py_stats import config


class TestGenerateCmds(unittest.TestCase):
    """
    Unit test class for testing the functionality of the generate_cmds module
    """

    def setUp(self):
        # Mock configuration for testing
        self.mock_config = {
            "since": "--since=2020-01-01",
            "until": "--until=2024-12-31",
            "merges": "--no-merges",
            "log_options": "",
            "pathspec": "--",
            "limit": 10,
            "menu_theme": "",
        }

    # Silence stdout and mock git command output
    @patch("git_py_stats.generate_cmds.run_git_command")
    @patch("git_py_stats.generate_cmds.print")
    def test_detailed_git_stats(self, mock_print, mock_run_git_command) -> None:
        """
        Test case for detailed_git_stats in generate_cmds.

        Checks if `detailed_git_stats` executes without errors and returns `None`.
        Print is mocked to prevent actual output during testing.

        Verifies that the function returns `None` and that print was called at least once.
        """
        # Mock git command output to ensure that print statements are executed
        mock_run_git_command.return_value = (
            "abc123\tJohn Doe\tjohn@example.com\t1609459200\n" "10\t0\tsomefile.py\n"
        )

        # Call function with mock configuration
        self.assertIsNone(generate_cmds.detailed_git_stats(self.mock_config))
        mock_print.assert_called()  # Check if print was called at least once

    # Silence stdout and mock git command output
    @patch("git_py_stats.generate_cmds.run_git_command")
    @patch("git_py_stats.generate_cmds.print")
    def test_changelogs(self, mock_print, mock_run_git_command) -> None:
        """
        Test case for changelogs in generate_cmds.

        Checks if `changelogs` executes without errors and returns `None`.
        Print is mocked to prevent actual output during testing.

        Verifies that the function returns `None` and that print was called at least once.
        """
        # Mock git command output
        mock_run_git_command.return_value = "2020-01-01\n2020-01-02"

        # Call function with mock configuration
        self.assertIsNone(generate_cmds.changelogs(self.mock_config))
        mock_print.assert_called()  # Check if print was called at least once


if __name__ == "__main__":
    unittest.main()
