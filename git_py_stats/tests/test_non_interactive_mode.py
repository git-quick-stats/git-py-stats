import unittest
from unittest.mock import patch
from argparse import Namespace

from git_py_stats import non_interactive_mode


class TestNonInteractiveMode(unittest.TestCase):
    """
    Unit test class for testing the non_interactive_mode module.
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

        # Default arguments with all options set to False or None
        self.all_args = {
            "detailed_git_stats": False,
            "git_stats_by_branch": None,
            "changelogs": False,
            "changelogs_by_author": None,
            "my_daily_stats": False,
            "csv_output_by_branch": False,
            "json_output": False,
            "branch_tree": False,
            "branches_by_date": False,
            "contributors": False,
            "new_contributors": None,
            "commits_per_author": False,
            "commits_per_day": False,
            "commits_by_year": False,
            "commits_by_month": False,
            "commits_by_weekday": False,
            "commits_by_author_by_weekday": None,
            "commits_by_hour": False,
            "commits_by_author_by_hour": None,
            "commits_by_timezone": False,
            "commits_by_author_by_timezone": None,
            "suggest_reviewers": False,
            "commits_calendar_by_author": None,
            "commits_heatmap": None,
        }

    @patch("git_py_stats.non_interactive_mode.generate_cmds.detailed_git_stats")
    def test_detailed_git_stats(self, mock_detailed_git_stats):
        args_dict = self.all_args.copy()
        args_dict["detailed_git_stats"] = True
        args = Namespace(**args_dict)
        non_interactive_mode.handle_non_interactive_mode(args, self.mock_config)
        mock_detailed_git_stats.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.non_interactive_mode.generate_cmds.detailed_git_stats")
    def test_git_stats_by_branch(self, mock_detailed_git_stats):
        args_dict = self.all_args.copy()
        args_dict["git_stats_by_branch"] = "develop"
        args = Namespace(**args_dict)
        non_interactive_mode.handle_non_interactive_mode(args, self.mock_config)
        mock_detailed_git_stats.assert_called_once_with(self.mock_config, "develop")

    @patch("git_py_stats.non_interactive_mode.generate_cmds.changelogs")
    def test_changelogs(self, mock_changelogs):
        args_dict = self.all_args.copy()
        args_dict["changelogs"] = True
        args = Namespace(**args_dict)
        non_interactive_mode.handle_non_interactive_mode(args, self.mock_config)
        mock_changelogs.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.non_interactive_mode.generate_cmds.changelogs")
    def test_changelogs_by_author(self, mock_changelogs):
        args_dict = self.all_args.copy()
        args_dict["changelogs_by_author"] = "John Doe"
        args = Namespace(**args_dict)
        non_interactive_mode.handle_non_interactive_mode(args, self.mock_config)
        mock_changelogs.assert_called_once_with(self.mock_config, "John Doe")

    @patch("git_py_stats.non_interactive_mode.generate_cmds.my_daily_status")
    def test_my_daily_stats(self, mock_my_daily_status):
        args_dict = self.all_args.copy()
        args_dict["my_daily_stats"] = True
        args = Namespace(**args_dict)
        non_interactive_mode.handle_non_interactive_mode(args, self.mock_config)
        mock_my_daily_status.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.non_interactive_mode.generate_cmds.output_daily_stats_csv")
    def test_csv_output_by_branch(self, mock_output_csv):
        args_dict = self.all_args.copy()
        args_dict["csv_output_by_branch"] = True
        args = Namespace(**args_dict)
        non_interactive_mode.handle_non_interactive_mode(args, self.mock_config)
        mock_output_csv.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.non_interactive_mode.generate_cmds.save_git_log_output_json")
    def test_json_output(self, mock_save_json):
        args_dict = self.all_args.copy()
        args_dict["json_output"] = True
        args = Namespace(**args_dict)
        non_interactive_mode.handle_non_interactive_mode(args, self.mock_config)
        mock_save_json.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.non_interactive_mode.calendar_cmds.commits_calendar_by_author")
    def test_commits_calendar_by_author(self, mock_commits_calendar_by_author):
        args_dict = self.all_args.copy()
        args_dict["commits_calendar_by_author"] = "John Doe"
        args = Namespace(**args_dict)
        non_interactive_mode.handle_non_interactive_mode(args, self.mock_config)
        mock_commits_calendar_by_author.assert_called_once_with(self.mock_config, "John Doe")

    @patch("git_py_stats.non_interactive_mode.calendar_cmds.commits_heatmap")
    def test_commits_heatmap(self, mock_commits_heatmap):
        args_dict = self.all_args.copy()
        args_dict["commits_heatmap"] = True
        args = Namespace(**args_dict)
        non_interactive_mode.handle_non_interactive_mode(args, self.mock_config)
        mock_commits_heatmap.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.non_interactive_mode.list_cmds.branch_tree")
    def test_branch_tree(self, mock_branch_tree):
        args_dict = self.all_args.copy()
        args_dict["branch_tree"] = True
        args = Namespace(**args_dict)
        non_interactive_mode.handle_non_interactive_mode(args, self.mock_config)
        mock_branch_tree.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.non_interactive_mode.list_cmds.branches_by_date")
    def test_branches_by_date(self, mock_branches_by_date):
        args_dict = self.all_args.copy()
        args_dict["branches_by_date"] = True
        args = Namespace(**args_dict)
        non_interactive_mode.handle_non_interactive_mode(args, self.mock_config)
        mock_branches_by_date.assert_called_once_with()

    @patch("git_py_stats.non_interactive_mode.list_cmds.contributors")
    def test_contributors(self, mock_contributors):
        args_dict = self.all_args.copy()
        args_dict["contributors"] = True
        args = Namespace(**args_dict)
        non_interactive_mode.handle_non_interactive_mode(args, self.mock_config)
        mock_contributors.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.non_interactive_mode.list_cmds.new_contributors")
    def test_new_contributors(self, mock_new_contributors):
        args_dict = self.all_args.copy()
        args_dict["new_contributors"] = "2021-01-01"
        args = Namespace(**args_dict)
        non_interactive_mode.handle_non_interactive_mode(args, self.mock_config)
        mock_new_contributors.assert_called_once_with(self.mock_config, "2021-01-01")

    @patch("git_py_stats.non_interactive_mode.list_cmds.git_commits_per_author")
    def test_commits_per_author(self, mock_commits_per_author):
        args_dict = self.all_args.copy()
        args_dict["commits_per_author"] = True
        args = Namespace(**args_dict)
        non_interactive_mode.handle_non_interactive_mode(args, self.mock_config)
        mock_commits_per_author.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.non_interactive_mode.list_cmds.git_commits_per_date")
    def test_commits_per_day(self, mock_commits_per_date):
        args_dict = self.all_args.copy()
        args_dict["commits_per_day"] = True
        args = Namespace(**args_dict)
        non_interactive_mode.handle_non_interactive_mode(args, self.mock_config)
        mock_commits_per_date.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.non_interactive_mode.list_cmds.git_commits_per_year")
    def test_commits_by_year(self, mock_commits_per_year):
        args_dict = self.all_args.copy()
        args_dict["commits_by_year"] = True
        args = Namespace(**args_dict)
        non_interactive_mode.handle_non_interactive_mode(args, self.mock_config)
        mock_commits_per_year.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.non_interactive_mode.list_cmds.git_commits_per_month")
    def test_commits_by_month(self, mock_commits_per_month):
        args_dict = self.all_args.copy()
        args_dict["commits_by_month"] = True
        args = Namespace(**args_dict)
        non_interactive_mode.handle_non_interactive_mode(args, self.mock_config)
        mock_commits_per_month.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.non_interactive_mode.list_cmds.git_commits_per_weekday")
    def test_commits_by_weekday(self, mock_commits_per_weekday):
        args_dict = self.all_args.copy()
        args_dict["commits_by_weekday"] = True
        args = Namespace(**args_dict)
        non_interactive_mode.handle_non_interactive_mode(args, self.mock_config)
        mock_commits_per_weekday.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.non_interactive_mode.list_cmds.git_commits_per_weekday")
    def test_commits_by_author_by_weekday(self, mock_commits_per_weekday):
        args_dict = self.all_args.copy()
        args_dict["commits_by_author_by_weekday"] = "Jane Smith"
        args = Namespace(**args_dict)
        non_interactive_mode.handle_non_interactive_mode(args, self.mock_config)
        mock_commits_per_weekday.assert_called_once_with(self.mock_config, "Jane Smith")

    @patch("git_py_stats.non_interactive_mode.list_cmds.git_commits_per_hour")
    def test_commits_by_hour(self, mock_commits_per_hour):
        args_dict = self.all_args.copy()
        args_dict["commits_by_hour"] = True
        args = Namespace(**args_dict)
        non_interactive_mode.handle_non_interactive_mode(args, self.mock_config)
        mock_commits_per_hour.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.non_interactive_mode.list_cmds.git_commits_per_hour")
    def test_commits_by_author_by_hour(self, mock_commits_per_hour):
        args_dict = self.all_args.copy()
        args_dict["commits_by_author_by_hour"] = "John Doe"
        args = Namespace(**args_dict)
        non_interactive_mode.handle_non_interactive_mode(args, self.mock_config)
        mock_commits_per_hour.assert_called_once_with(self.mock_config, "John Doe")

    @patch("git_py_stats.non_interactive_mode.list_cmds.git_commits_per_timezone")
    def test_commits_by_timezone(self, mock_commits_per_timezone):
        args_dict = self.all_args.copy()
        args_dict["commits_by_timezone"] = True
        args = Namespace(**args_dict)
        non_interactive_mode.handle_non_interactive_mode(args, self.mock_config)
        mock_commits_per_timezone.assert_called_once_with(self.mock_config)

    @patch("git_py_stats.non_interactive_mode.list_cmds.git_commits_per_timezone")
    def test_commits_by_author_by_timezone(self, mock_commits_per_timezone):
        args_dict = self.all_args.copy()
        args_dict["commits_by_author_by_timezone"] = "Alice"
        args = Namespace(**args_dict)
        non_interactive_mode.handle_non_interactive_mode(args, self.mock_config)
        mock_commits_per_timezone.assert_called_once_with(self.mock_config, "Alice")

    @patch("git_py_stats.non_interactive_mode.suggest_cmds.suggest_reviewers")
    def test_suggest_reviewers(self, mock_suggest_reviewers):
        args_dict = self.all_args.copy()
        args_dict["suggest_reviewers"] = True
        args = Namespace(**args_dict)
        non_interactive_mode.handle_non_interactive_mode(args, self.mock_config)
        mock_suggest_reviewers.assert_called_once_with(self.mock_config)

    @patch("builtins.print")
    @patch("git_py_stats.non_interactive_mode.ArgumentParser")
    def test_invalid_option(self, mock_argument_parser, mock_print):
        args_dict = self.all_args.copy()
        args = Namespace(**args_dict)
        non_interactive_mode.handle_non_interactive_mode(args, self.mock_config)

        # Verify that "Invalid option provided.\n" was printed
        mock_print.assert_called_once_with("Invalid option provided.\n")

        # Verify that ArgumentParser was instantiated and print_help was called
        mock_argument_parser.return_value.print_help.assert_called_once()


if __name__ == "__main__":
    unittest.main()
