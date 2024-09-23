import unittest
from unittest.mock import patch
import datetime

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
    def test_changelogs(self, mock_print) -> None:
        """
        Test case for changelogs in generate_cmds.

        Checks if `changelogs` executes without errors and returns `None`.
        Print is mocked to prevent actual output during testing.

        Verifies that the function returns `None` and that print was called at least once.
        """
        
        self.assertIsNone(generate_cmds.changelogs())
        mock_print.assert_called()


if __name__ == '__main__':
    unittest.main()

