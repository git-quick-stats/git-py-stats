import unittest
from unittest.mock import patch

from git_py_stats import list_cmds


class TestListCmds(unittest.TestCase):
    """
    Unit test class for testing list_cmds.
    """

    # Prevent printing to stdout
    @patch('git_py_stats.list_cmds.print')
    def test_branch_tree_view(self, mock_print) -> None:
        """
        Test case for the branch_tree_view function in the list_cmds module.

        Checks if `branch_tree_view` executes without errors and returns `None`.
        The print function is mocked to prevent actual output during testing.

        The test verifies that the function runs without raising any exceptions and
        calls the print function at least once, indicating that some output was generated.
        """
        
        # TODO: We can probably handle this a bit better. Basic test for now, though
        self.assertIsNone(list_cmds.branch_tree_view())
        mock_print.assert_called()

if __name__ == '__main__':
    unittest.main()

