import unittest
from unittest.mock import patch, MagicMock
from git_py_stats import suggest_cmds


class TestSuggestCmds(unittest.TestCase):
    """
    Unit test class for testing suggest_cmds
    """

    def setUp(self):
        # Mock configuration for testing
        self.mock_config = {
            'since': '--since=2020-01-01',
            'until': '--until=2024-12-31',
            'merges': '--no-merges',
            'log_options': '',
            'pathspec': '--',
        }

    # Don't print to stdout and mock git command output
    @patch('git_py_stats.suggest_cmds.run_git_command')
    @patch('git_py_stats.suggest_cmds.print')
    def test_suggest_reviewers(self, mock_print, mock_run_git_command) -> None:
        """
        Test case for suggest_reviewers in suggest_cmds.

        Checks if `suggest_reviewers` executes without errors, and it uses
        `unittest.mock.patch` to mock the print function to prevent actual
        output during testing.

        Verifies that the function returns `None` and calls the print function
        at least once, indicating that some output was generated.
        """
        # Mock git command output to provide a list of authors
        mock_run_git_command.return_value = (
            "Alice\nBob\nAlice\nCharlie\nBob\nBob\n"
        )

        # Call function with mock configuration
        suggest_cmds.suggest_reviewers(self.mock_config)
        
        # Assert that print was called at least once
        mock_print.assert_called()

if __name__ == '__main__':
    unittest.main()

