import unittest
from unittest.mock import patch

from git_py_stats import suggest_cmds


class TestSuggestCmds(unittest.TestCase):
    """
    Unit test class for testing suggest_cmds
    """

    # Don't print to stdout
    @patch('git_py_stats.suggest_cmds.print')
    def test_suggest_reviewers(self, mock_print) -> None:
        """
        Test case for suggest_reviewers in suggest_cmds

        Checks if `suggest_reviewers` executes without errors, and it uses
        `unittest.mock.patch` to mock the print function to prevent actual
        output during testing.

        Verifies that the function returns `None` and calls the print function
        at least once, indicating that some output was generated.
        """
        
        result = suggest_cmds.suggest_reviewers()
        self.assertIsNone(result)
        mock_print.assert_called()

if __name__ == '__main__':
    unittest.main()

