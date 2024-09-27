import unittest
from unittest.mock import patch, MagicMock

from git_py_stats import suggest_cmds


class TestSuggestCmds(unittest.TestCase):
    """
    Unit test class for testing suggest_cmds.
    """

    def setUp(self):
        # Mock configuration for testing
        self.mock_config = {
            "since": "--since=2020-01-01",
            "until": "--until=2024-12-31",
            "merges": "--no-merges",
            "log_options": "",
            "pathspec": "--",
        }

    @patch("git_py_stats.suggest_cmds.print")
    @patch("git_py_stats.suggest_cmds.run_git_command")
    def test_suggest_reviewers_normal_case(self, mock_run_git_command, mock_print):
        """
        Test suggest_reviewers with typical git output.
        """
        # Mock git command output with multiple authors
        mock_run_git_command.return_value = "Alice\nBob\nAlice\nCharlie\nBob\nBob\n"

        # Expected output after processing
        expected_output = [
            "Suggested code reviewers based on git history:",
            "      3 Bob",
            "      2 Alice",
            "      1 Charlie",
        ]

        suggest_cmds.suggest_reviewers(self.mock_config)

        # Verify that print was called with the expected output
        mock_print.assert_any_call("Suggested code reviewers based on git history:")
        mock_print.assert_any_call("      3 Bob")
        mock_print.assert_any_call("      2 Alice")
        mock_print.assert_any_call("      1 Charlie")

    @patch("git_py_stats.suggest_cmds.print")
    @patch("git_py_stats.suggest_cmds.run_git_command")
    def test_suggest_reviewers_no_output(self, mock_run_git_command, mock_print):
        """
        Test suggest_reviewers when git command returns no output.
        """
        mock_run_git_command.return_value = ""

        suggest_cmds.suggest_reviewers(self.mock_config)

        # Verify that print was called with "No data available."
        mock_print.assert_called_once_with("No data available.")

    @patch("git_py_stats.suggest_cmds.print")
    @patch("git_py_stats.suggest_cmds.run_git_command")
    def test_suggest_reviewers_no_authors_found(self, mock_run_git_command, mock_print):
        """
        Test suggest_reviewers when no authors are found after processing.
        """
        mock_run_git_command.return_value = "\n"  # Only newline characters

        suggest_cmds.suggest_reviewers(self.mock_config)

        # Verify that print was called with "No potential reviewers found."
        mock_print.assert_called_once_with("No potential reviewers found.")

    @patch("git_py_stats.suggest_cmds.print")
    @patch("git_py_stats.suggest_cmds.run_git_command")
    def test_suggest_reviewers_single_author(self, mock_run_git_command, mock_print):
        """
        Test suggest_reviewers with only one author in git output.
        """
        mock_run_git_command.return_value = "Alice\nAlice\nAlice\n"

        suggest_cmds.suggest_reviewers(self.mock_config)

        # Verify the output
        mock_print.assert_any_call("Suggested code reviewers based on git history:")
        mock_print.assert_any_call("      3 Alice")

    @patch("git_py_stats.suggest_cmds.print")
    @patch("git_py_stats.suggest_cmds.run_git_command")
    def test_suggest_reviewers_handles_exceptions(self, mock_run_git_command, mock_print):
        """
        Test suggest_reviewers when run_git_command returns None (simulating an exception).
        """
        mock_run_git_command.return_value = None

        suggest_cmds.suggest_reviewers(self.mock_config)

        # Verify that "No data available." was printed
        mock_print.assert_called_once_with("No data available.")

    @patch("git_py_stats.suggest_cmds.print")
    @patch("git_py_stats.suggest_cmds.run_git_command")
    def test_suggest_reviewers_large_number_of_authors(self, mock_run_git_command, mock_print):
        """
        Test suggest_reviewers with more than 100 authors.
        """
        # Create a list of 150 authors
        authors = [f"Author_{i%10}" for i in range(150)]  # 10 unique authors repeated
        mock_run_git_command.return_value = "\n".join(authors)

        suggest_cmds.suggest_reviewers(self.mock_config)

        # Ensure that only the top 100 commits are considered
        # So counts will be based on the first 100 entries
        counts = {f"Author_{i}": 0 for i in range(10)}
        for i in range(100):
            counts[authors[i]] += 1

        # Prepare expected outputs
        expected_output = ["Suggested code reviewers based on git history:"]
        sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
        for author, count in sorted_counts:
            expected_output.append(f"{count:7} {author}")

        # Verify that print was called with expected outputs
        mock_print.assert_any_call("Suggested code reviewers based on git history:")
        for line in expected_output[1:]:
            mock_print.assert_any_call(line)

    @patch("git_py_stats.suggest_cmds.print")
    @patch("git_py_stats.suggest_cmds.run_git_command")
    def test_suggest_reviewers_authors_with_same_count(self, mock_run_git_command, mock_print):
        """
        Test suggest_reviewers when authors have the same commit count.
        """
        mock_run_git_command.return_value = "Bob\nAlice\nCharlie\nBob\nAlice\nCharlie\n"

        suggest_cmds.suggest_reviewers(self.mock_config)

        # Since all have 2 commits, they should be sorted by name
        expected_output = [
            "Suggested code reviewers based on git history:",
            "      2 Alice",
            "      2 Bob",
            "      2 Charlie",
        ]

        # Verify that print was called with expected outputs
        mock_print.assert_any_call("Suggested code reviewers based on git history:")
        for line in expected_output[1:]:
            mock_print.assert_any_call(line)

    @patch("git_py_stats.suggest_cmds.print")
    @patch("git_py_stats.suggest_cmds.run_git_command")
    def test_suggest_reviewers_non_standard_characters(self, mock_run_git_command, mock_print):
        """
        Test suggest_reviewers with author names containing non-standard characters.
        """
        mock_run_git_command.return_value = "José\nMüller\n李四\nO'Connor\nJosé\n"

        suggest_cmds.suggest_reviewers(self.mock_config)

        expected_output = [
            "Suggested code reviewers based on git history:",
            "      2 José",
            "      1 Müller",
            "      1 O'Connor",
            "      1 李四",
        ]

        mock_print.assert_any_call("Suggested code reviewers based on git history:")
        for line in expected_output[1:]:
            mock_print.assert_any_call(line)

    @patch("git_py_stats.suggest_cmds.print")
    @patch("git_py_stats.suggest_cmds.run_git_command")
    def test_suggest_reviewers_handles_empty_lines(self, mock_run_git_command, mock_print):
        """
        Test suggest_reviewers when git output contains empty lines.
        """
        mock_run_git_command.return_value = "Alice\n\nBob\n\nAlice\n"

        suggest_cmds.suggest_reviewers(self.mock_config)

        expected_output = [
            "Suggested code reviewers based on git history:",
            "      2 Alice",
            "      1 Bob",
        ]

        mock_print.assert_any_call("Suggested code reviewers based on git history:")
        for line in expected_output[1:]:
            mock_print.assert_any_call(line)

    @patch("git_py_stats.suggest_cmds.print")
    @patch("git_py_stats.suggest_cmds.run_git_command")
    def test_suggest_reviewers_handles_whitespace(self, mock_run_git_command, mock_print):
        """
        Test suggest_reviewers when author names have leading/trailing whitespace.
        """
        mock_run_git_command.return_value = "  Alice  \nBob\nAlice\n"

        suggest_cmds.suggest_reviewers(self.mock_config)

        # Expect that the leading/trailing whitespace is preserved
        expected_output = [
            "Suggested code reviewers based on git history:",
            "      2 Alice",
            "      1 Bob",
        ]

        mock_print.assert_any_call("Suggested code reviewers based on git history:")
        for line in expected_output[1:]:
            mock_print.assert_any_call(line)


if __name__ == "__main__":
    unittest.main()

