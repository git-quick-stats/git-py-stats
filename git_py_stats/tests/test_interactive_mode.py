import unittest
from unittest.mock import patch

from git_py_stats import interactive_mode


class TestInteractiveMode(unittest.TestCase):
    """
    Unit test class for testing the interactive_mode module.
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

    @patch("git_py_stats.interactive_mode.interactive_menu")
    @patch("builtins.input")
    @patch("git_py_stats.generate_cmds.detailed_git_stats")
    def test_option_1(self, mock_detailed_git_stats, mock_input, mock_interactive_menu):
        # Simulate user selecting option '1' and then exiting
        mock_interactive_menu.side_effect = ["1", ""]
        interactive_mode.handle_interactive_mode(self.mock_config)
        mock_detailed_git_stats.assert_called_once_with(self.mock_config)
        mock_input.assert_not_called()

    @patch("git_py_stats.interactive_mode.interactive_menu")
    @patch("builtins.input", return_value="develop")
    @patch("git_py_stats.generate_cmds.detailed_git_stats")
    def test_option_2(self, mock_detailed_git_stats, mock_input, mock_interactive_menu):
        mock_interactive_menu.side_effect = ["2", ""]
        interactive_mode.handle_interactive_mode(self.mock_config)
        mock_detailed_git_stats.assert_called_once_with(self.mock_config, "develop")
        mock_input.assert_called_once_with("Enter branch name: ")

    @patch("git_py_stats.interactive_mode.interactive_menu")
    @patch("git_py_stats.generate_cmds.changelogs")
    def test_option_3(self, mock_changelogs, mock_interactive_menu):
        mock_interactive_menu.side_effect = ["3", ""]
        interactive_mode.handle_interactive_mode(self.mock_config)
        mock_changelogs.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.interactive_mode.interactive_menu")
    @patch("builtins.input", return_value="John Doe")
    @patch("git_py_stats.generate_cmds.changelogs")
    def test_option_4(self, mock_changelogs, mock_input, mock_interactive_menu):
        mock_interactive_menu.side_effect = ["4", ""]
        interactive_mode.handle_interactive_mode(self.mock_config)
        mock_changelogs.assert_called_once_with(self.mock_config, "John Doe")
        mock_input.assert_called_once_with("Enter author name: ")

    @patch("git_py_stats.interactive_mode.interactive_menu")
    @patch("git_py_stats.generate_cmds.my_daily_status")
    def test_option_5(self, mock_my_daily_status, mock_interactive_menu):
        mock_interactive_menu.side_effect = ["5", ""]
        interactive_mode.handle_interactive_mode(self.mock_config)
        mock_my_daily_status.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.interactive_mode.interactive_menu")
    @patch("git_py_stats.generate_cmds.output_daily_stats_csv")
    def test_option_6(self, mock_output_csv, mock_interactive_menu):
        mock_interactive_menu.side_effect = ["6", ""]
        interactive_mode.handle_interactive_mode(self.mock_config)
        mock_output_csv.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.interactive_mode.interactive_menu")
    @patch("git_py_stats.generate_cmds.save_git_log_output_json")
    def test_option_7(self, mock_save_json, mock_interactive_menu):
        mock_interactive_menu.side_effect = ["7", ""]
        interactive_mode.handle_interactive_mode(self.mock_config)
        mock_save_json.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.interactive_mode.interactive_menu")
    @patch("git_py_stats.list_cmds.branch_tree")
    def test_option_8(self, mock_branch_tree, mock_interactive_menu):
        mock_interactive_menu.side_effect = ["8", ""]
        interactive_mode.handle_interactive_mode(self.mock_config)
        mock_branch_tree.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.interactive_mode.interactive_menu")
    @patch("git_py_stats.list_cmds.branches_by_date")
    def test_option_9(self, mock_branches_by_date, mock_interactive_menu):
        mock_interactive_menu.side_effect = ["9", ""]
        interactive_mode.handle_interactive_mode(self.mock_config)
        mock_branches_by_date.assert_called_once_with()

    @patch("git_py_stats.interactive_mode.interactive_menu")
    @patch("git_py_stats.list_cmds.contributors")
    def test_option_10(self, mock_contributors, mock_interactive_menu):
        mock_interactive_menu.side_effect = ["10", ""]
        interactive_mode.handle_interactive_mode(self.mock_config)
        mock_contributors.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.interactive_mode.interactive_menu")
    @patch("builtins.input", return_value="2021-01-01")
    @patch("git_py_stats.list_cmds.new_contributors")
    def test_option_11(self, mock_new_contributors, mock_input, mock_interactive_menu):
        mock_interactive_menu.side_effect = ["11", ""]
        interactive_mode.handle_interactive_mode(self.mock_config)
        mock_new_contributors.assert_called_once_with(self.mock_config, "2021-01-01")
        mock_input.assert_called_once_with("Enter cutoff date (YYYY-MM-DD): ")

    @patch("git_py_stats.interactive_mode.interactive_menu")
    @patch("git_py_stats.list_cmds.git_commits_per_author")
    def test_option_12(self, mock_commits_per_author, mock_interactive_menu):
        mock_interactive_menu.side_effect = ["12", ""]
        interactive_mode.handle_interactive_mode(self.mock_config)
        mock_commits_per_author.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.interactive_mode.interactive_menu")
    @patch("git_py_stats.list_cmds.git_commits_per_date")
    def test_option_13(self, mock_commits_per_date, mock_interactive_menu):
        mock_interactive_menu.side_effect = ["13", ""]
        interactive_mode.handle_interactive_mode(self.mock_config)
        mock_commits_per_date.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.interactive_mode.interactive_menu")
    @patch("git_py_stats.list_cmds.git_commits_per_month")
    def test_option_14(self, mock_commits_per_month, mock_interactive_menu):
        mock_interactive_menu.side_effect = ["14", ""]
        interactive_mode.handle_interactive_mode(self.mock_config)
        mock_commits_per_month.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.interactive_mode.interactive_menu")
    @patch("git_py_stats.list_cmds.git_commits_per_year")
    def test_option_15(self, mock_commits_per_year, mock_interactive_menu):
        mock_interactive_menu.side_effect = ["15", ""]
        interactive_mode.handle_interactive_mode(self.mock_config)
        mock_commits_per_year.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.interactive_mode.interactive_menu")
    @patch("git_py_stats.list_cmds.git_commits_per_weekday")
    def test_option_16(self, mock_commits_per_weekday, mock_interactive_menu):
        mock_interactive_menu.side_effect = ["16", ""]
        interactive_mode.handle_interactive_mode(self.mock_config)
        mock_commits_per_weekday.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.interactive_mode.interactive_menu")
    @patch("builtins.input", return_value="Alice")
    @patch("git_py_stats.list_cmds.git_commits_per_weekday")
    def test_option_17(self, mock_commits_per_weekday, mock_input, mock_interactive_menu):
        mock_interactive_menu.side_effect = ["17", ""]
        interactive_mode.handle_interactive_mode(self.mock_config)
        mock_commits_per_weekday.assert_called_once_with(self.mock_config, "Alice")
        mock_input.assert_called_once_with("Enter author name: ")

    @patch("git_py_stats.interactive_mode.interactive_menu")
    @patch("git_py_stats.list_cmds.git_commits_per_hour")
    def test_option_18(self, mock_commits_per_hour, mock_interactive_menu):
        mock_interactive_menu.side_effect = ["18", ""]
        interactive_mode.handle_interactive_mode(self.mock_config)
        mock_commits_per_hour.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.interactive_mode.interactive_menu")
    @patch("builtins.input", return_value="Bob")
    @patch("git_py_stats.list_cmds.git_commits_per_hour")
    def test_option_19(self, mock_commits_per_hour, mock_input, mock_interactive_menu):
        mock_interactive_menu.side_effect = ["19", ""]
        interactive_mode.handle_interactive_mode(self.mock_config)
        mock_commits_per_hour.assert_called_once_with(self.mock_config, "Bob")
        mock_input.assert_called_once_with("Enter author name: ")

    @patch("git_py_stats.interactive_mode.interactive_menu")
    @patch("git_py_stats.list_cmds.git_commits_per_timezone")
    def test_option_20(self, mock_commits_per_timezone, mock_interactive_menu):
        mock_interactive_menu.side_effect = ["20", ""]
        interactive_mode.handle_interactive_mode(self.mock_config)
        mock_commits_per_timezone.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.interactive_mode.interactive_menu")
    @patch("builtins.input", return_value="Charlie")
    @patch("git_py_stats.list_cmds.git_commits_per_timezone")
    def test_option_21(self, mock_commits_per_timezone, mock_input, mock_interactive_menu):
        mock_interactive_menu.side_effect = ["21", ""]
        interactive_mode.handle_interactive_mode(self.mock_config)
        mock_commits_per_timezone.assert_called_once_with(self.mock_config, "Charlie")
        mock_input.assert_called_once_with("Enter author name: ")

    @patch("git_py_stats.interactive_mode.interactive_menu")
    @patch("git_py_stats.suggest_cmds.suggest_reviewers")
    def test_option_22(self, mock_suggest_reviewers, mock_interactive_menu):
        mock_interactive_menu.side_effect = ["22", ""]
        interactive_mode.handle_interactive_mode(self.mock_config)
        mock_suggest_reviewers.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.interactive_mode.interactive_menu")
    @patch("builtins.print")
    def test_invalid_option(self, mock_print, mock_interactive_menu):
        mock_interactive_menu.side_effect = ["invalid", ""]
        interactive_mode.handle_interactive_mode(self.mock_config)
        mock_print.assert_called_with("Invalid selection. Please try again.")

    @patch("git_py_stats.interactive_mode.interactive_menu")
    def test_exit(self, mock_interactive_menu):
        mock_interactive_menu.side_effect = ["", ""]
        interactive_mode.handle_interactive_mode(self.mock_config)
        mock_interactive_menu.assert_called_once_with(self.mock_config)


if __name__ == "__main__":
    unittest.main()

