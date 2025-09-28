import unittest
from unittest.mock import patch, mock_open
import json

from git_py_stats import generate_cmds


class TestGenerateCmds(unittest.TestCase):
    """
    Unit test class for testing the functionality of the generate_cmds module
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

    def _extract_printed_authors(self, mock_print):
        """
        Return the list of author display lines in the order they were printed.
        """
        authors = []
        for call in mock_print.call_args_list:
            msg = call.args[0] if call.args else ""
            # lines look like "         John Doe <john@example.com>:"
            if isinstance(msg, str) and msg.strip().endswith(">:"):
                authors.append(msg.strip()[:-1])  # drop trailing ":"
        return authors

    @patch("git_py_stats.generate_cmds.run_git_command")
    @patch("builtins.print")
    def test_sort_by_commits_desc(self, mock_print, mock_run_git_command):
        """
        Test detailed_git_stats when sorting by commits in descending order.
        """
        # Two authors, B has more commits but fewer insertions
        mock_run_git_command.return_value = (
            # A1 (2 commits total)
            "c1\tAlice\talice@example.com\t1609459200\n"
            "10\t1\ta.py\n"
            "c2\tAlice\talice@example.com\t1609459300\n"
            "5\t0\ta2.py\n"
            # B1 (3 commits total)
            "c3\tBob\tbob@example.com\t1609460000\n"
            "1\t1\tb.py\n"
            "c4\tBob\tbob@example.com\t1609460100\n"
            "2\t2\tb2.py\n"
            "c5\tBob\tbob@example.com\t1609460200\n"
            "3\t3\tb3.py\n"
        )

        cfg = dict(self.mock_config)
        cfg["sort_by"] = "commits"
        cfg["sort_dir"] = "desc"

        generate_cmds.detailed_git_stats(cfg)

        authors = self._extract_printed_authors(mock_print)
        # Expect Bob first (3 commits) then Alice (2)
        self.assertGreaterEqual(len(authors), 2)
        self.assertTrue(authors[0].startswith("Bob <bob@example.com>"))
        self.assertTrue(authors[1].startswith("Alice <alice@example.com>"))
        # Header shows sort choice
        printed = " ".join(a.args[0] for a in mock_print.call_args_list if a.args)
        self.assertIn("Sorting by: commits (desc)", printed)

    @patch("git_py_stats.generate_cmds.run_git_command")
    @patch("builtins.print")
    def test_sort_by_lines_asc_with_name_tiebreaker(self, mock_print, mock_run_git_command):
        """
        Test detailed_git_stats when sorting by lines in ascending order.
        Attempts to handle a "tiebreaker" when sorting by falling back to
        the person's name in ascending order. So if Alice and Bob have the
        same number of commits, Alice should be chosen.
        """
        mock_run_git_command.return_value = (
            # Alice: 3+3 = 6 lines
            "c1\tAlice\talice@example.com\t1609459200\n"
            "3\t3\ta.py\n"
            # Bob: 4+2 = 6 lines
            "c2\tBob\tbob@example.com\t1609460000\n"
            "4\t2\tb.py\n"
        )

        cfg = dict(self.mock_config)
        cfg["sort_by"] = "lines"
        cfg["sort_dir"] = "asc"

        generate_cmds.detailed_git_stats(cfg)

        authors = self._extract_printed_authors(mock_print)
        self.assertGreaterEqual(len(authors), 2)
        self.assertTrue(authors[0].startswith("Alice <alice@example.com>"))
        self.assertTrue(authors[1].startswith("Bob <bob@example.com>"))
        printed = " ".join(a.args[0] for a in mock_print.call_args_list if a.args)
        self.assertIn("Sorting by: lines (asc)", printed)

    @patch("git_py_stats.generate_cmds.run_git_command")
    @patch("builtins.print")
    def test_sort_by_name_desc(self, mock_print, mock_run_git_command):
        """
        Test detailed_git_stats when sorting by name in descending order.
        """
        mock_run_git_command.return_value = (
            "c1\tAlice\talice@example.com\t1609459200\n"
            "1\t0\ta.py\n"
            "c2\tBob\tbob@example.com\t1609460000\n"
            "1\t0\tb.py\n"
            "c3\tCarol\tcarol@example.com\t1609470000\n"
            "1\t0\tc.py\n"
        )

        cfg = dict(self.mock_config)
        cfg["sort_by"] = "name"
        cfg["sort_dir"] = "desc"

        generate_cmds.detailed_git_stats(cfg)

        authors = self._extract_printed_authors(mock_print)
        # Descending name: Carol, Bob, Alice
        self.assertTrue(authors[0].startswith("Carol <carol@example.com>"))
        self.assertTrue(authors[1].startswith("Bob <bob@example.com>"))
        self.assertTrue(authors[2].startswith("Alice <alice@example.com>"))

    @patch("git_py_stats.generate_cmds.run_git_command")
    @patch("builtins.print")
    def test_detailed_git_stats(self, mock_print, mock_run_git_command):
        """
        Test detailed_git_stats function with sample git output.
        """
        # Mock git command output
        mock_output = (
            "abc123\tJohn Doe\tjohn@example.com\t1609459200\n"
            "10\t2\tsomefile.py\n"
            "def456\tJane Smith\tjane@example.com\t1609545600\n"
            "5\t3\tanotherfile.py\n"
        )
        mock_run_git_command.return_value = mock_output

        generate_cmds.detailed_git_stats(self.mock_config)

        # Check that print was called
        self.assertTrue(mock_print.called)
        # You can add more detailed assertions based on the expected outputs

    @patch("git_py_stats.generate_cmds.run_git_command")
    @patch("builtins.print")
    def test_detailed_git_stats_no_output(self, mock_print, mock_run_git_command):
        """
        Test detailed_git_stats when git command returns no output.
        """
        mock_run_git_command.return_value = ""

        generate_cmds.detailed_git_stats(self.mock_config)

        # Should not raise an error and print nothing
        self.assertFalse(mock_print.called)

    @patch("git_py_stats.generate_cmds.run_git_command")
    @patch("builtins.print")
    def test_changelogs(self, mock_print, mock_run_git_command):
        """
        Test changelogs function with sample git output.
        """
        mock_run_git_command.side_effect = [
            "2021-01-02\n2021-01-01",  # Dates output
            "* Commit message 1 (John Doe)\n* Commit message 2 (Jane Smith)",  # First date commits
            "* Commit message 3 (John Doe)",  # Second date commits
        ]

        generate_cmds.changelogs(self.mock_config)

        self.assertTrue(mock_print.called)
        # You can add more detailed assertions based on the expected outputs

    @patch("git_py_stats.generate_cmds.run_git_command")
    @patch("builtins.print")
    def test_changelogs_no_commits(self, mock_print, mock_run_git_command):
        """
        Test changelogs when git command returns no commits.
        """
        mock_run_git_command.return_value = ""

        generate_cmds.changelogs(self.mock_config)

        # Verify that "No commits found." was printed
        mock_print.assert_any_call("No commits found.")

    @patch("git_py_stats.generate_cmds.run_git_command")
    @patch("builtins.print")
    def test_changelogs_with_author(self, mock_print, mock_run_git_command):
        """
        Test changelogs function with an author specified.
        """
        mock_run_git_command.side_effect = [
            "2021-01-01",  # Dates output
            "* Commit message 1 (John Doe)",  # Commits for date
        ]

        generate_cmds.changelogs(self.mock_config, author="John Doe")

        # Verify that the author option was included in the command
        called_cmd = mock_run_git_command.call_args_list[0][0][0]
        self.assertIn("--author=John Doe", called_cmd)

        self.assertTrue(mock_print.called)

    @patch("git_py_stats.generate_cmds.run_git_command")
    @patch("builtins.print")
    def test_my_daily_status(self, mock_print, mock_run_git_command):
        """
        Test my_daily_status function with sample git output.
        """
        # Mock git command outputs
        mock_run_git_command.side_effect = [
            "1 file changed, 10 insertions(+), 2 deletions(-)",  # git diff output
            "John Doe",  # git config user.name
            "abc123\ndef456",  # git log output with commit hashes
        ]

        generate_cmds.my_daily_status(self.mock_config)

        calls = [call.args[0] for call in mock_print.call_args_list]
        self.assertIn("My daily status:", calls)
        self.assertIn("\t1 file changed", calls)
        self.assertIn("\t10 insertions(+)", calls)
        self.assertIn("\t2 deletions(-)", calls)
        self.assertIn("\t2 commits", calls)

    @patch("git_py_stats.generate_cmds.run_git_command")
    @patch("builtins.print")
    def test_my_daily_status_no_changes(self, mock_print, mock_run_git_command):
        """
        Test my_daily_status when there are no changes or commits.
        """
        # Mock git command outputs
        mock_run_git_command.side_effect = [
            "",  # git diff output (no changes)
            "John Doe",  # git config user.name
            "",  # git log output (no commits)
        ]

        generate_cmds.my_daily_status(self.mock_config)

        calls = [call.args[0] for call in mock_print.call_args_list]
        self.assertIn("My daily status:", calls)
        self.assertIn("\tNo changes in the last day.", calls)
        self.assertIn("\t0 commits", calls)

    @patch("git_py_stats.generate_cmds.run_git_command")
    @patch("builtins.input", return_value="")
    @patch("builtins.print")
    def test_output_daily_stats_csv(self, mock_print, mock_input, mock_run_git_command):
        """
        Test output_daily_stats_csv function with sample git output.
        """
        mock_run_git_command.return_value = "2021-01-01\n2021-01-01\n2021-01-02\n2021-01-03\n"

        # Mock open to prevent actual file creation
        with patch("builtins.open", mock_open()) as mocked_file:
            generate_cmds.output_daily_stats_csv(self.mock_config)

            # Check that file was written
            mocked_file.assert_called_with("git_daily_stats.csv", "w", newline="")

            # Check that print was called
            self.assertTrue(mock_print.called)
            mock_print.assert_any_call("Daily stats saved to git_daily_stats.csv")

    @patch("git_py_stats.generate_cmds.run_git_command")
    @patch("builtins.input", return_value="")
    @patch("builtins.print")
    def test_output_daily_stats_csv_no_data(self, mock_print, mock_input, mock_run_git_command):
        """
        Test output_daily_stats_csv when git command returns no data.
        """
        mock_run_git_command.return_value = ""

        generate_cmds.output_daily_stats_csv(self.mock_config)

        mock_print.assert_called_once_with("No data available.")

    @patch("git_py_stats.generate_cmds.run_git_command")
    @patch("builtins.print")
    def test_save_git_log_output_json(self, mock_print, mock_run_git_command):
        """
        Test save_git_log_output_json function with sample git output.
        """
        mock_run_git_command.return_value = (
            "abc123|John Doe|2021-01-01 12:00:00 +0000|Commit message 1\n"
            "def456|Jane Smith|2021-01-02 13:00:00 +0000|Commit message 2\n"
        )

        # Mock open to prevent actual file creation
        with patch("builtins.open", mock_open()) as mocked_file:
            generate_cmds.save_git_log_output_json(self.mock_config)

            # Check that file was written
            mocked_file.assert_called_with("git_log.json", "w")

            # Verify that json.dump was called
            handle = mocked_file()
            handle.write.assert_called()
            written_data = "".join(call.args[0] for call in handle.write.call_args_list)
            data = json.loads(written_data)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]["hash"], "abc123")

            # Check that print was called
            self.assertTrue(mock_print.called)
            mock_print.assert_any_call("Git log saved to git_log.json")

    @patch("git_py_stats.generate_cmds.run_git_command")
    @patch("builtins.print")
    def test_save_git_log_output_json_no_data(self, mock_print, mock_run_git_command):
        """
        Test save_git_log_output_json when git command returns no data.
        """
        mock_run_git_command.return_value = ""

        generate_cmds.save_git_log_output_json(self.mock_config)

        mock_print.assert_called_once_with("No log data available.")

    @patch("git_py_stats.generate_cmds.run_git_command")
    @patch("builtins.print")
    def test_detailed_git_stats_handles_invalid_lines(self, mock_print, mock_run_git_command):
        """
        Test detailed_git_stats with invalid lines in git output.
        """
        mock_output = (
            "invalid line without tabs\n"
            "abc123\tJohn Doe\tjohn@example.com\t1609459200\n"
            "invalid\tdata\n"
            "5\t3\tfile.py\n"
        )
        mock_run_git_command.return_value = mock_output

        generate_cmds.detailed_git_stats(self.mock_config)

        self.assertTrue(mock_print.called)

    @patch("git_py_stats.generate_cmds.run_git_command")
    @patch("builtins.print")
    def test_my_daily_status_user_unknown(self, mock_print, mock_run_git_command):
        """
        Test my_daily_status when git user.name is not set.
        """
        # Mock git command outputs
        mock_run_git_command.side_effect = [
            "",  # git diff output (no changes)
            None,  # git config user.name returns None
            "",  # git log output (no commits)
        ]

        generate_cmds.my_daily_status(self.mock_config)

        # Check that '--author=unknown' is used in the git log command
        log_cmd = mock_run_git_command.call_args_list[2][0][0]
        self.assertIn("--author=unknown", log_cmd)

    @patch("git_py_stats.generate_cmds.run_git_command")
    @patch("builtins.input", return_value="")
    @patch("builtins.print")
    def test_output_daily_stats_csv_io_error(self, mock_print, mock_input, mock_run_git_command):
        """
        Test output_daily_stats_csv when an IOError occurs during file writing.
        """
        mock_run_git_command.return_value = "2021-01-01\n2021-01-02"

        with patch("builtins.open", side_effect=IOError("Disk full")):
            generate_cmds.output_daily_stats_csv(self.mock_config)

            mock_print.assert_any_call("Failed to write to git_daily_stats.csv: Disk full")

    @patch("git_py_stats.generate_cmds.run_git_command")
    @patch("builtins.print")
    def test_save_git_log_output_json_io_error(self, mock_print, mock_run_git_command):
        """
        Test save_git_log_output_json when an IOError occurs during file writing.
        """
        mock_run_git_command.return_value = (
            "abc123|John Doe|2021-01-01 12:00:00 +0000|Commit message 1\n"
        )

        with patch("builtins.open", side_effect=IOError("Disk full")):
            generate_cmds.save_git_log_output_json(self.mock_config)

            mock_print.assert_any_call("Failed to write to git_log.json: Disk full")


if __name__ == "__main__":
    unittest.main()
