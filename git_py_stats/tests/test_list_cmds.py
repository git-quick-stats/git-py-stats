import unittest
from unittest.mock import patch, MagicMock
from git_py_stats import list_cmds


class TestListCmds(unittest.TestCase):
    """
    Unit test class for testing list_cmds.
    """

    def setUp(self):
        # Mock configuration for testing
        self.mock_config = {
            'since': '--since=2020-01-01',
            'until': '--until=2024-12-31',
            'merges': '--no-merges',
            'log_options': '',
            'pathspec': '--',
            'limit': 10
        }

    # Prevent printing to stdout and mock git command output
    @patch('git_py_stats.list_cmds.run_git_command')
    @patch('git_py_stats.list_cmds.print')
    def test_branch_tree(self, mock_print, mock_run_git_command) -> None:
        """
        Test case for the branch_tree function in the list_cmds module.

        Checks if `branch_tree` executes without errors and returns `None`.
        The print function is mocked to prevent actual output during testing.

        The test verifies that the function runs without raising any exceptions and
        calls the print function at least once, indicating that some output was generated.
        """
        # Mock git command output to provide a sample branch tree
        mock_run_git_command.return_value = (
            "* 12345 Commit message\n"
            "| * 67890 Another commit message\n"
            "| * abcde Yet another commit message\n"
        )

        # Call function with mock configuration
        list_cmds.branch_tree(self.mock_config)

        # Assert that print was called at least once
        mock_print.assert_called()

if __name__ == '__main__':
    unittest.main()

