import unittest
from unittest.mock import patch
import io

from git_py_stats.arg_parser import parse_arguments


class TestArgParser(unittest.TestCase):
    """
    Unit test class for testing the argument parser functionality.
    """

    def test_no_arguments(self):
        """
        Test parsing with no arguments.

        This ensures that all options have their default values when no
        command-line arguments are provided.
        """
        args = parse_arguments([])
        self.assertFalse(args.detailed_git_stats)
        self.assertIsNone(args.git_stats_by_branch)
        self.assertFalse(args.changelogs)
        self.assertIsNone(args.changelogs_by_author)
        self.assertFalse(args.my_daily_stats)
        self.assertFalse(args.csv_output_by_branch)
        self.assertFalse(args.json_output)
        self.assertFalse(args.branch_tree)
        self.assertFalse(args.branches_by_date)
        self.assertFalse(args.contributors)
        self.assertIsNone(args.new_contributors)
        self.assertFalse(args.commits_per_author)
        self.assertFalse(args.commits_per_day)
        self.assertFalse(args.commits_by_year)
        self.assertFalse(args.commits_by_month)
        self.assertFalse(args.commits_by_weekday)
        self.assertIsNone(args.commits_by_author_by_weekday)
        self.assertFalse(args.commits_by_hour)
        self.assertIsNone(args.commits_by_author_by_hour)
        self.assertFalse(args.commits_by_timezone)
        self.assertIsNone(args.commits_by_author_by_timezone)
        self.assertFalse(args.suggest_reviewers)

    def test_detailed_git_stats(self):
        """
        Test the --detailed-git-stats and -T options.
        """
        args = parse_arguments(["--detailed-git-stats"])
        self.assertTrue(args.detailed_git_stats)

        args = parse_arguments(["-T"])
        self.assertTrue(args.detailed_git_stats)

        args = parse_arguments([])
        self.assertFalse(args.detailed_git_stats)

    def test_git_stats_by_branch(self):
        """
        Test the --git-stats-by-branch and -R options.
        """
        args = parse_arguments(["--git-stats-by-branch", "main"])
        self.assertEqual(args.git_stats_by_branch, "main")

        args = parse_arguments(["-R", "develop"])
        self.assertEqual(args.git_stats_by_branch, "develop")

        with self.assertRaises(SystemExit) as cm:
            parse_arguments(["--git-stats-by-branch"])
        self.assertEqual(cm.exception.code, 2)

    def test_changelogs(self):
        """
        Test the --changelogs and -c options.
        """
        args = parse_arguments(["--changelogs"])
        self.assertTrue(args.changelogs)

        args = parse_arguments(["-c"])
        self.assertTrue(args.changelogs)

        args = parse_arguments([])
        self.assertFalse(args.changelogs)

    def test_changelogs_by_author(self):
        """
        Test the --changelogs-by-author and -L options.
        """
        args = parse_arguments(["--changelogs-by-author", "John Doe"])
        self.assertEqual(args.changelogs_by_author, "John Doe")

        args = parse_arguments(["-L", "Jane Smith"])
        self.assertEqual(args.changelogs_by_author, "Jane Smith")

        with self.assertRaises(SystemExit) as cm:
            parse_arguments(["--changelogs-by-author"])
        self.assertEqual(cm.exception.code, 2)

    def test_my_daily_stats(self):
        """
        Test the --my-daily-stats and -S options.
        """
        args = parse_arguments(["--my-daily-stats"])
        self.assertTrue(args.my_daily_stats)

        args = parse_arguments(["-S"])
        self.assertTrue(args.my_daily_stats)

        args = parse_arguments([])
        self.assertFalse(args.my_daily_stats)

    def test_csv_output_by_branch(self):
        """
        Test the --csv-output-by-branch and -V options.
        """
        args = parse_arguments(["--csv-output-by-branch"])
        self.assertTrue(args.csv_output_by_branch)

        args = parse_arguments(["-V"])
        self.assertTrue(args.csv_output_by_branch)

        args = parse_arguments([])
        self.assertFalse(args.csv_output_by_branch)

    def test_json_output(self):
        """
        Test the --json-output and -j options.
        """
        args = parse_arguments(["--json-output"])
        self.assertTrue(args.json_output)

        args = parse_arguments(["-j"])
        self.assertTrue(args.json_output)

        args = parse_arguments([])
        self.assertFalse(args.json_output)

    def test_branch_tree(self):
        """
        Test the --branch-tree and -b options.
        """
        args = parse_arguments(["--branch-tree"])
        self.assertTrue(args.branch_tree)

        args = parse_arguments(["-b"])
        self.assertTrue(args.branch_tree)

        args = parse_arguments([])
        self.assertFalse(args.branch_tree)

    def test_branches_by_date(self):
        """
        Test the --branches-by-date and -D options.
        """
        args = parse_arguments(["--branches-by-date"])
        self.assertTrue(args.branches_by_date)

        args = parse_arguments(["-D"])
        self.assertTrue(args.branches_by_date)

        args = parse_arguments([])
        self.assertFalse(args.branches_by_date)

    def test_contributors(self):
        """
        Test the --contributors and -C options.
        """
        args = parse_arguments(["--contributors"])
        self.assertTrue(args.contributors)

        args = parse_arguments(["-C"])
        self.assertTrue(args.contributors)

        args = parse_arguments([])
        self.assertFalse(args.contributors)

    def test_new_contributors(self):
        """
        Test the --new-contributors and -n options.
        """
        args = parse_arguments(["--new-contributors", "2021-01-01"])
        self.assertEqual(args.new_contributors, "2021-01-01")

        args = parse_arguments(["-n", "2020-12-31"])
        self.assertEqual(args.new_contributors, "2020-12-31")

        with self.assertRaises(SystemExit) as cm:
            parse_arguments(["--new-contributors"])
        self.assertEqual(cm.exception.code, 2)

    def test_commits_per_author(self):
        """
        Test the --commits-per-author and -a options.
        """
        args = parse_arguments(["--commits-per-author"])
        self.assertTrue(args.commits_per_author)

        args = parse_arguments(["-a"])
        self.assertTrue(args.commits_per_author)

        args = parse_arguments([])
        self.assertFalse(args.commits_per_author)

    def test_commits_per_day(self):
        """
        Test the --commits-per-day and -d options.
        """
        args = parse_arguments(["--commits-per-day"])
        self.assertTrue(args.commits_per_day)

        args = parse_arguments(["-d"])
        self.assertTrue(args.commits_per_day)

        args = parse_arguments([])
        self.assertFalse(args.commits_per_day)

    def test_commits_by_year(self):
        """
        Test the --commits-by-year and -Y options.
        """
        args = parse_arguments(["--commits-by-year"])
        self.assertTrue(args.commits_by_year)

        args = parse_arguments(["-Y"])
        self.assertTrue(args.commits_by_year)

        args = parse_arguments([])
        self.assertFalse(args.commits_by_year)

    def test_commits_by_month(self):
        """
        Test the --commits-by-month and -m options.
        """
        args = parse_arguments(["--commits-by-month"])
        self.assertTrue(args.commits_by_month)

        args = parse_arguments(["-m"])
        self.assertTrue(args.commits_by_month)

        args = parse_arguments([])
        self.assertFalse(args.commits_by_month)

    def test_commits_by_weekday(self):
        """
        Test the --commits-by-weekday and -w options.
        """
        args = parse_arguments(["--commits-by-weekday"])
        self.assertTrue(args.commits_by_weekday)

        args = parse_arguments(["-w"])
        self.assertTrue(args.commits_by_weekday)

        args = parse_arguments([])
        self.assertFalse(args.commits_by_weekday)

    def test_commits_by_author_by_weekday(self):
        """
        Test the --commits-by-author-by-weekday and -W options.
        """
        args = parse_arguments(["--commits-by-author-by-weekday", "John Doe"])
        self.assertEqual(args.commits_by_author_by_weekday, "John Doe")

        args = parse_arguments(["-W", "Jane Smith"])
        self.assertEqual(args.commits_by_author_by_weekday, "Jane Smith")

        with self.assertRaises(SystemExit) as cm:
            parse_arguments(["--commits-by-author-by-weekday"])
        self.assertEqual(cm.exception.code, 2)

    def test_commits_by_hour(self):
        """
        Test the --commits-by-hour and -o options.
        """
        args = parse_arguments(["--commits-by-hour"])
        self.assertTrue(args.commits_by_hour)

        args = parse_arguments(["-o"])
        self.assertTrue(args.commits_by_hour)

        args = parse_arguments([])
        self.assertFalse(args.commits_by_hour)

    def test_commits_by_author_by_hour(self):
        """
        Test the --commits-by-author-by-hour and -A options.
        """
        args = parse_arguments(["--commits-by-author-by-hour", "John Doe"])
        self.assertEqual(args.commits_by_author_by_hour, "John Doe")

        args = parse_arguments(["-A", "Jane Smith"])
        self.assertEqual(args.commits_by_author_by_hour, "Jane Smith")

        with self.assertRaises(SystemExit) as cm:
            parse_arguments(["--commits-by-author-by-hour"])
        self.assertEqual(cm.exception.code, 2)

    def test_commits_by_timezone(self):
        """
        Test the --commits-by-timezone and -z options.
        """
        args = parse_arguments(["--commits-by-timezone"])
        self.assertTrue(args.commits_by_timezone)

        args = parse_arguments(["-z"])
        self.assertTrue(args.commits_by_timezone)

        args = parse_arguments([])
        self.assertFalse(args.commits_by_timezone)

    def test_commits_by_author_by_timezone(self):
        """
        Test the --commits-by-author-by-timezone and -Z options.
        """
        args = parse_arguments(["--commits-by-author-by-timezone", "John Doe"])
        self.assertEqual(args.commits_by_author_by_timezone, "John Doe")

        args = parse_arguments(["-Z", "Jane Smith"])
        self.assertEqual(args.commits_by_author_by_timezone, "Jane Smith")

        with self.assertRaises(SystemExit) as cm:
            parse_arguments(["--commits-by-author-by-timezone"])
        self.assertEqual(cm.exception.code, 2)

    def test_suggest_reviewers(self):
        """
        Test the --suggest-reviewers and -r options.
        """
        args = parse_arguments(["--suggest-reviewers"])
        self.assertTrue(args.suggest_reviewers)

        args = parse_arguments(["-r"])
        self.assertTrue(args.suggest_reviewers)

        args = parse_arguments([])
        self.assertFalse(args.suggest_reviewers)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_help_option(self, mock_stdout):
        """
        Test the --help option.
        """
        with self.assertRaises(SystemExit) as cm:
            parse_arguments(["--help"])
        self.assertEqual(cm.exception.code, 0)
        output = mock_stdout.getvalue()
        self.assertIn("usage:", output)
        self.assertIn("Git Py Stats - A Python Implementation of Git Quick Stats.", output)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_short_help_option(self, mock_stdout):
        """
        Test the -h option.
        """
        with self.assertRaises(SystemExit) as cm:
            parse_arguments(["-h"])
        self.assertEqual(cm.exception.code, 0)
        output = mock_stdout.getvalue()
        self.assertIn("usage:", output)
        self.assertIn("Git Py Stats - A Python Implementation of Git Quick Stats.", output)

    def test_unknown_argument(self):
        """
        Test passing an unknown argument.
        """
        with self.assertRaises(SystemExit) as cm:
            parse_arguments(["--unknown-option"])
        self.assertEqual(cm.exception.code, 2)

        with self.assertRaises(SystemExit) as cm:
            parse_arguments(["-X"])
        self.assertEqual(cm.exception.code, 2)

    def test_multiple_options(self):
        """
        Test combining multiple options.
        """
        args = parse_arguments(["-T", "-c", "--my-daily-stats"])
        self.assertTrue(args.detailed_git_stats)
        self.assertTrue(args.changelogs)
        self.assertTrue(args.my_daily_stats)
        self.assertFalse(args.csv_output_by_branch)
        self.assertIsNone(args.git_stats_by_branch)

    def test_repeated_options(self):
        """
        Test passing the same option multiple times.
        """
        args = parse_arguments(["-T", "--detailed-git-stats"])
        self.assertTrue(args.detailed_git_stats)

    def test_empty_string_argument(self):
        """
        Test passing an empty string as an argument.
        """
        args = parse_arguments(["--git-stats-by-branch", ""])
        self.assertEqual(args.git_stats_by_branch, "")

    def test_argument_starting_with_dash(self):
        """
        Test passing an argument that starts with a dash.
        """
        args = parse_arguments(["--git-stats-by-branch=-develop"])
        self.assertEqual(args.git_stats_by_branch, "-develop")

    def test_author_name_with_spaces(self):
        """
        Test passing an author name with spaces.
        """
        args = parse_arguments(["--changelogs-by-author", "John Doe"])
        self.assertEqual(args.changelogs_by_author, "John Doe")

        args = parse_arguments(["--changelogs-by-author", "José María"])
        self.assertEqual(args.changelogs_by_author, "José María")


if __name__ == "__main__":
    unittest.main()
