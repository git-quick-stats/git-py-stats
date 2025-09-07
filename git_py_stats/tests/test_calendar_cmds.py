import unittest
from unittest.mock import patch
from datetime import datetime

from git_py_stats import calendar_cmds


class TestCalendarCmds(unittest.TestCase):
    """
    Unit test class for testing the functionality of the calendar_cmds module
    """

    def setUp(self):
        # Mock configuration for testing
        self.mock_config = {
            "since": "--since=2020-01-01",
            "until": "--until=2024-12-31",
            "merges": "--no-merges",
            "log_options": "",
            "pathspec": "--",
            "limit": 10,  # Ensure limit is an integer
            "menu_theme": "",
        }

    @patch("git_py_stats.calendar_cmds.run_git_command")
    @patch("builtins.print")
    def test_commits_calendar_by_author(self, mock_print, mock_run_git_command):
        """
        Test commits_calendar_by_author function with an author specified.
        """
        # Mock git command outputs
        mock_run_git_command.side_effect = [
            "",  # git diff output (no changes)
            "John Doe",  # git config user.name
            "",  # git log output (no commits)
        ]

        calendar_cmds.commits_calendar_by_author(self.mock_config, author="John Doe")

        # Verify that the author option was included in the command
        called_cmd = mock_run_git_command.call_args_list[0][0][0]
        self.assertIn("--author=John Doe", called_cmd)

        self.assertTrue(mock_print.called)

    # HEATMAP HELPER FUNCTIONS
    def _freeze_today(self, y: int, m: int, d: int):
        """
        Patch calendar_cmds.datetime.now() to a fixed date (keeps strptime intact).
        """

        class _FixedDT(datetime):
            @classmethod
            def now(cls, tz=None):
                return cls(y, m, d, 12, 0, 0)

        # Swap datetime in the module
        self._orig_datetime = calendar_cmds.datetime
        calendar_cmds.datetime = _FixedDT
        self.addCleanup(self._restore_datetime)

    def _restore_datetime(self):
        if hasattr(self, "_orig_datetime"):
            calendar_cmds.datetime = self._orig_datetime

    @patch("git_py_stats.calendar_cmds.run_git_command")
    @patch("builtins.print")
    def test_commits_heatmap_invokes_git_per_day_and_prints_header(
        self, mock_print, mock_run_git_command
    ):
        """
        With days=2 and today fixed to 2024-01-03, expect two git calls:
        for 2024-01-02 and 2024-01-03. Also validate header and row stubs.
        """
        # Freeze "today" as 2024-01-03 (Wed)
        self._freeze_today(2024, 1, 3)
        cfg = dict(self.mock_config, days=2)

        # First day has two commits; second day none.
        mock_run_git_command.side_effect = [
            "2024-01-02 00:15:00 +0000\n2024-01-02 15:20:00 +0000",
            "",
        ]

        calendar_cmds.commits_heatmap(cfg)

        # Two calls total (one per day)
        self.assertEqual(mock_run_git_command.call_count, 2)

        # Validate the first command args
        first_cmd = mock_run_git_command.call_args_list[0][0][0]
        self.assertIn("git", first_cmd)
        self.assertIn("-c", first_cmd)
        self.assertIn("log.showSignature=false", first_cmd)
        self.assertIn("log", first_cmd)
        self.assertIn("--use-mailmap", first_cmd)
        self.assertIn("--no-merges", first_cmd)
        self.assertIn("--pretty=%ci", first_cmd)
        self.assertIn("--since=2024-01-02 00:00", first_cmd)
        self.assertIn("--until=2024-01-02 23:59", first_cmd)
        self.assertIn("--", first_cmd)  # pathspec

        # Validate the second command args (today)
        second_cmd = mock_run_git_command.call_args_list[1][0][0]
        self.assertIn("--since=2024-01-03 00:00", second_cmd)
        self.assertIn("--until=2024-01-03 23:59", second_cmd)

        # Stitch printed output to a single string for simple assertions
        out = "\n".join(" ".join(map(str, c.args)) for c in mock_print.call_args_list)

        # Title and header
        self.assertIn("Commit Heatmap for the last 2 days", out)
        self.assertIn("Day | Date/Hours |", out)
        # Row headers (ignore ANSI codes beyond substring check)
        self.assertIn("Tue | 2024-01-02 |", out)
        self.assertIn("Wed | 2024-01-03 |", out)

    @patch("git_py_stats.calendar_cmds.run_git_command", return_value="")
    @patch("builtins.print")
    def test_commits_heatmap_weekend_rows_are_gray(self, mock_print, _mock_run):
        """
        When the single rendered day is a Saturday, the line should start
        with the 256-color gray prefix (38;5;240m).
        """
        # Freeze to a Saturday: 2024-01-06
        self._freeze_today(2024, 1, 6)
        cfg = dict(self.mock_config, days=1)

        calendar_cmds.commits_heatmap(cfg)

        out = "\n".join(" ".join(map(str, c.args)) for c in mock_print.call_args_list)
        # Gray prefix must appear before "Sat | 2024-01-06 |"
        self.assertIn("\x1b[38;5;240mSat | 2024-01-06 |", out)

    @patch("git_py_stats.calendar_cmds.run_git_command", return_value="")
    @patch("builtins.print")
    def test_commits_heatmap_respects_days_setting(self, _mock_print, mock_run):
        """
        If days=3, run_git_command is called exactly 3 times (one per day).
        """
        # Freeze some arbitrary date
        self._freeze_today(2024, 5, 10)
        cfg = dict(self.mock_config, days=3)

        calendar_cmds.commits_heatmap(cfg)

        self.assertEqual(mock_run.call_count, 3)


if __name__ == "__main__":
    unittest.main()
