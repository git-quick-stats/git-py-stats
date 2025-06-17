import unittest
from unittest.mock import patch
from io import StringIO
import re

from git_py_stats.menu import interactive_menu


def strip_ansi_codes(text):
    """
    Remove ANSI escape codes from text. Necessary because, without this,
    capturing sys.stdout would capture the string with the raw ANSI
    along with it, causing our assertions to fail.
    """
    ansi_escape = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
    return ansi_escape.sub("", text)


class TestInteractiveMenu(unittest.TestCase):
    """
    Unit test class for testing the interactive_menu function in menu.py.
    """

    def setUp(self):
        # Mock configurations for testing
        self.config_default = {}  # Default theme
        self.config_legacy = {"menu_theme": "legacy"}  # Legacy theme
        self.config_none = {"menu_theme": "none"}  # Alternate colorless theme alias

    @patch("builtins.input", return_value="1")
    @patch("sys.stdout", new_callable=StringIO)
    def test_default_theme_option_1(self, mock_stdout, mock_input):
        """
        Test the interactive_menu with default theme and user selects option '1'.
        """
        choice = interactive_menu(self.config_default)
        self.assertEqual(choice, "1")
        output = strip_ansi_codes(mock_stdout.getvalue())

        # Check that the menu contains specific text
        self.assertIn("Generate:", output)
        self.assertIn("1) Contribution stats (by author)", output)
        self.assertIn("press Enter to exit", output)

    @patch("builtins.input", return_value="22")
    @patch("sys.stdout", new_callable=StringIO)
    def test_default_theme_option_22(self, mock_stdout, mock_input):
        """
        Test the interactive_menu with default theme and user selects option '22'.
        """
        choice = interactive_menu(self.config_default)
        self.assertEqual(choice, "22")
        output = strip_ansi_codes(mock_stdout.getvalue())
        self.assertIn("Suggest:", output)
        self.assertIn("22) Code reviewers (based on git history)", output)

    @patch("builtins.input", return_value="")
    @patch("sys.stdout", new_callable=StringIO)
    def test_default_theme_exit(self, mock_stdout, mock_input):
        """
        Test the interactive_menu with default theme and user presses Enter to exit.
        """
        choice = interactive_menu(self.config_default)
        self.assertEqual(choice, "")
        output = strip_ansi_codes(mock_stdout.getvalue())
        self.assertIn("press Enter to exit", output)

    @patch("builtins.input", return_value="invalid")
    @patch("sys.stdout", new_callable=StringIO)
    def test_default_theme_invalid_input(self, mock_stdout, mock_input):
        """
        Test the interactive_menu with default theme and user enters an invalid option.
        """
        choice = interactive_menu(self.config_default)
        self.assertEqual(choice, "invalid")
        # Since interactive_menu doesn't print 'Invalid selection', we don't assert that here.
        output = strip_ansi_codes(mock_stdout.getvalue())
        self.assertIn("Generate:", output)

    @patch("builtins.input", return_value="1")
    @patch("sys.stdout", new_callable=StringIO)
    def test_legacy_theme_option_1(self, mock_stdout, mock_input):
        """
        Test the interactive_menu with legacy theme and user selects option '1'.
        """
        choice = interactive_menu(self.config_legacy)
        self.assertEqual(choice, "1")
        output = strip_ansi_codes(mock_stdout.getvalue())
        self.assertIn("Generate:", output)
        self.assertIn("1) Contribution stats (by author)", output)

    @patch("builtins.input", return_value="3")
    @patch("sys.stdout", new_callable=StringIO)
    def test_none_theme_option_3(self, mock_stdout, mock_input):
        """
        Test the interactive_menu with 'none' theme (alias for colorless) and user selects option '3'.
        """
        choice = interactive_menu(self.config_none)
        self.assertEqual(choice, "3")
        output = mock_stdout.getvalue()
        self.assertNotIn("\033[31m", output)  # No RED
        self.assertNotIn("\033[33m", output)  # No YELLOW
        self.assertNotIn("\033[36m", output)  # No CYAN
        self.assertIn("\033[1m", output)      # BOLD allowed

if __name__ == "__main__":
    unittest.main()
