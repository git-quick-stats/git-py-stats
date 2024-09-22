import unittest
from unittest.mock import patch

from git_py_stats import generate_cmds


class TestGenerateCmds(unittest.TestCase):
    """
    Unit test class for testing the functionality of the generate_cmds module
    """

    # Silence stdout
    @patch('git_py_stats.generate_cmds.print')
    def test_contribution_stats_by_author(self, mock_print) -> None:
        """
        Test case for contribution_stats_by_author in generate_cmds.

        Checks if `contribution_stats_by_author` executes without errors and returns `None`.
        Print is mocked to prevent actual output during testing.

        Verifies that the function returns `None` and that print was called at least once.
        """
        
        self.assertIsNone(generate_cmds.contribution_stats_by_author())
        mock_print.assert_called()

    # Silence stdout
    @patch('git_py_stats.generate_cmds.print')
    def test_git_changelogs_last_10_days(self, mock_print) -> None:
        """
        Test case for git_changelogs_last_10_days in generate_cmds.

        Checks if `git_changelogs_last_10_days` executes without errors and returns `None`.
        Print is mocked to prevent actual output during testing.

        Verifies that the function returns `None` and that print was called at least once.
        """
        
        self.assertIsNone(generate_cmds.git_changelogs_last_10_days())
        mock_print.assert_called()


if __name__ == '__main__':
    unittest.main()

