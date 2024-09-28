import unittest
from unittest.mock import patch
from git_py_stats import list_cmds


class TestListCmds(unittest.TestCase):
    """
    Unit test class for testing list_cmds functions.
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
        }

    # Prevent printing to stdout and mock git command output
    @patch("git_py_stats.list_cmds.run_git_command")
    @patch("git_py_stats.list_cmds.print")
    def test_branch_tree(self, mock_print, mock_run_git_command) -> None:
        """
        Test case for the branch_tree function.
        """
        mock_run_git_command.return_value = (
            "* 12345 Commit message\n"
            "| * 67890 Another commit message\n"
            "| * abcde Yet another commit message\n"
        )

        list_cmds.branch_tree(self.mock_config)

        mock_print.assert_called()
        mock_run_git_command.assert_called_once()

    @patch("git_py_stats.list_cmds.run_git_command")
    @patch("git_py_stats.list_cmds.print")
    def test_branch_tree_no_data(self, mock_print, mock_run_git_command) -> None:
        """
        Test case for branch_tree with no data.
        """
        mock_run_git_command.return_value = ""
        list_cmds.branch_tree(self.mock_config)

        mock_print.assert_called_with("No data available.")

    @patch("git_py_stats.list_cmds.run_git_command")
    @patch("git_py_stats.list_cmds.print")
    def test_branches_by_date(self, mock_print, mock_run_git_command) -> None:
        """
        Test case for branches_by_date function.
        """
        mock_run_git_command.return_value = (
            "[2021-01-01] Author1 branch1\n" "[2021-01-02] Author2 branch2\n"
        )
        list_cmds.branches_by_date()

        mock_print.assert_called()
        mock_run_git_command.assert_called_once()

    @patch("git_py_stats.list_cmds.run_git_command")
    @patch("git_py_stats.list_cmds.print")
    def test_branches_by_date_no_data(self, mock_print, mock_run_git_command) -> None:
        """
        Test case for branches_by_date with no data.
        """
        mock_run_git_command.return_value = ""
        list_cmds.branches_by_date()

        mock_print.assert_called_with("No commits found.")

    @patch("git_py_stats.list_cmds.run_git_command")
    @patch("git_py_stats.list_cmds.print")
    def test_contributors(self, mock_print, mock_run_git_command) -> None:
        """
        Test case for the contributors function.
        """
        mock_run_git_command.return_value = "Author1\nAuthor2\nAuthor3\n"
        list_cmds.contributors(self.mock_config)

        mock_print.assert_called()
        mock_run_git_command.assert_called_once()

    @patch("git_py_stats.list_cmds.run_git_command")
    @patch("git_py_stats.list_cmds.print")
    def test_contributors_no_data(self, mock_print, mock_run_git_command) -> None:
        """
        Test case for contributors with no data.
        """
        mock_run_git_command.return_value = ""
        list_cmds.contributors(self.mock_config)

        mock_print.assert_called_with("No contributors found.")

    @patch("git_py_stats.list_cmds.run_git_command")
    @patch("git_py_stats.list_cmds.print")
    def test_new_contributors(self, mock_print, mock_run_git_command) -> None:
        """
        Test case for new_contributors function.
        """
        mock_run_git_command.return_value = "author1@example.com|1577836800\n"
        list_cmds.new_contributors(self.mock_config, "2020-01-01")

        mock_print.assert_called()
        mock_run_git_command.assert_called_once()

    @patch("git_py_stats.list_cmds.run_git_command")
    @patch("git_py_stats.list_cmds.print")
    def test_new_contributors_invalid_date(self, mock_print, mock_run_git_command) -> None:
        """
        Test case for new_contributors with invalid date.
        """
        list_cmds.new_contributors(self.mock_config, "invalid-date")

        mock_print.assert_called_with("Invalid date format. Please use YYYY-MM-DD.")
        mock_run_git_command.assert_not_called()

    @patch("git_py_stats.list_cmds.run_git_command")
    @patch("git_py_stats.list_cmds.print")
    def test_git_commits_per_author(self, mock_print, mock_run_git_command) -> None:
        """
        Test case for git_commits_per_author function.
        """
        mock_run_git_command.return_value = "Author:Author1 <author1@example.com>\n"
        list_cmds.git_commits_per_author(self.mock_config)

        mock_print.assert_called()
        mock_run_git_command.assert_called_once()

    @patch("git_py_stats.list_cmds.run_git_command")
    @patch("git_py_stats.list_cmds.print")
    def test_git_commits_per_author_no_data(self, mock_print, mock_run_git_command) -> None:
        """
        Test case for git_commits_per_author with no data.
        """
        mock_run_git_command.return_value = ""
        list_cmds.git_commits_per_author(self.mock_config)

        mock_print.assert_called_with("No commits found.")

    @patch("git_py_stats.list_cmds.run_git_command")
    @patch("git_py_stats.list_cmds.print")
    def test_git_commits_per_date(self, mock_print, mock_run_git_command) -> None:
        """
        Test case for git_commits_per_date function.
        """
        mock_run_git_command.return_value = "2021-01-01\n2021-01-01\n2021-01-02\n"
        list_cmds.git_commits_per_date(self.mock_config)

        mock_print.assert_called()
        mock_run_git_command.assert_called_once()

    @patch("git_py_stats.list_cmds.run_git_command")
    @patch("git_py_stats.list_cmds.print")
    def test_git_commits_per_date_no_data(self, mock_print, mock_run_git_command) -> None:
        """
        Test case for git_commits_per_date with no data.
        """
        mock_run_git_command.return_value = ""
        list_cmds.git_commits_per_date(self.mock_config)

        mock_print.assert_called_with("No commits found.")

    @patch("git_py_stats.list_cmds.run_git_command")
    @patch("git_py_stats.list_cmds.print")
    def test_git_commits_per_month(self, mock_print, mock_run_git_command) -> None:
        """
        Test case for git_commits_per_month function.
        """
        mock_run_git_command.return_value = "Jan\nJan\nFeb\n"
        list_cmds.git_commits_per_month(self.mock_config)

        mock_print.assert_called()
        mock_run_git_command.assert_called_once()

    @patch("git_py_stats.list_cmds.run_git_command")
    @patch("git_py_stats.list_cmds.print")
    def test_git_commits_per_year(self, mock_print, mock_run_git_command) -> None:
        """
        Test case for git_commits_per_year function.
        """
        mock_run_git_command.return_value = "2020\n2021\n2021\n2022\n"
        list_cmds.git_commits_per_year(self.mock_config)

        mock_print.assert_any_call("Git commits by year:\n")
        self.assertGreater(mock_print.call_count, 1)
        mock_run_git_command.assert_called_once()

    @patch("git_py_stats.list_cmds.run_git_command")
    @patch("git_py_stats.list_cmds.print")
    def test_git_commits_per_year_empty(self, mock_print, mock_run_git_command) -> None:
        """
        Test case for git_commits_per_year with empty data.
        """
        mock_run_git_command.return_value = ""  # No output
        list_cmds.git_commits_per_year(self.mock_config)

        mock_print.assert_called_with("No commits found.")
        mock_run_git_command.assert_called_once()

    @patch("git_py_stats.list_cmds.run_git_command")
    @patch("git_py_stats.list_cmds.print")
    def test_git_commits_per_year_invalid_data(self, mock_print, mock_run_git_command) -> None:
        """
        Test case for git_commits_per_year with invalid data.
        """
        mock_run_git_command.return_value = "\n\n\n"  # Invalid output, just new lines
        list_cmds.git_commits_per_year(self.mock_config)

        mock_print.assert_called_with("No valid years found in commits.")
        mock_run_git_command.assert_called_once()

    @patch("git_py_stats.list_cmds.run_git_command")
    @patch("git_py_stats.list_cmds.print")
    def test_git_commits_per_weekday(self, mock_print, mock_run_git_command) -> None:
        """
        Test case for git_commits_per_weekday function.
        """
        mock_run_git_command.return_value = "Mon\nTue\nWed\n"
        list_cmds.git_commits_per_weekday(self.mock_config)

        mock_print.assert_called()
        mock_run_git_command.assert_called_once()

    @patch("git_py_stats.list_cmds.run_git_command")
    @patch("git_py_stats.list_cmds.print")
    def test_git_commits_per_hour(self, mock_print, mock_run_git_command) -> None:
        """
        Test case for git_commits_per_hour function.
        """
        mock_run_git_command.return_value = "10\n11\n12\n"
        list_cmds.git_commits_per_hour(self.mock_config)

        mock_print.assert_called()
        mock_run_git_command.assert_called_once()

    @patch("git_py_stats.list_cmds.run_git_command")
    @patch("git_py_stats.list_cmds.print")
    def test_git_commits_per_timezone(self, mock_print, mock_run_git_command) -> None:
        """
        Test case for git_commits_per_timezone function.
        """
        mock_run_git_command.return_value = "+0200\n-0500\n+0200\n"
        list_cmds.git_commits_per_timezone(self.mock_config)

        mock_print.assert_called()
        mock_run_git_command.assert_called_once()


if __name__ == "__main__":
    unittest.main()
