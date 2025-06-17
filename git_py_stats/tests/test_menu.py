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
        self.assertNotIn("\033[31m", output)
        self.assertNotIn("\033[33m", output)
        self.assertNotIn("\033[36m", output)
        self.assertIn("\033[1m", output)

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

    @patch("builtins.input", return_value="2")
    @patch("sys.stdout", new_callable=StringIO)
    def test_legacy_theme_option_2(self, mock_stdout, mock_input):
        """
        Test the interactive_menu with legacy theme and user selects option '2'.
        """
        choice = interactive_menu(self.config_legacy)
        self.assertEqual(choice, "2")
        output = strip_ansi_codes(mock_stdout.getvalue())
        self.assertIn("2) Contribution stats (by author) on a specific branch", output)

    @patch("builtins.input", return_value="")
    @patch("sys.stdout", new_callable=StringIO)
    def test_legacy_theme_exit(self, mock_stdout, mock_input):
        """
        Test the interactive_menu with legacy theme and user presses Enter to exit.
        """
        choice = interactive_menu(self.config_legacy)
        self.assertEqual(choice, "")
        output = strip_ansi_codes(mock_stdout.getvalue())
        self.assertIn("press Enter to exit", output)

    @patch("builtins.input", return_value="invalid")
    @patch("sys.stdout", new_callable=StringIO)
    def test_legacy_theme_invalid_input(self, mock_stdout, mock_input):
        """
        Test the interactive_menu with legacy theme and user enters an invalid option.
        """
        choice = interactive_menu(self.config_legacy)
        self.assertEqual(choice, "invalid")
        output = strip_ansi_codes(mock_stdout.getvalue())
        self.assertIn("Generate:", output)

    @patch("builtins.input", side_effect=["1", ""])
    @patch("sys.stdout", new_callable=StringIO)
    def test_multiple_inputs(self, mock_stdout, mock_input):
        """
        Test the interactive_menu with multiple inputs in sequence.
        """
        choice1 = interactive_menu(self.config_default)
        choice2 = interactive_menu(self.config_default)
        self.assertEqual(choice1, "1")
        self.assertEqual(choice2, "")
        output = strip_ansi_codes(mock_stdout.getvalue())
        self.assertIn("Generate:", output)

    @patch("builtins.input", return_value="   5   ")
    @patch("sys.stdout", new_callable=StringIO)
    def test_input_with_whitespace(self, mock_stdout, mock_input):
        """
        Test the interactive_menu with input that includes leading/trailing whitespace.
        """
        choice = interactive_menu(self.config_default)
        self.assertEqual(choice, "5")
        output = strip_ansi_codes(mock_stdout.getvalue())
        self.assertIn("5) My daily status", output)

    @patch("builtins.input", return_value="QUIT")
    @patch("sys.stdout", new_callable=StringIO)
    def test_input_quit(self, mock_stdout, mock_input):
        """
        Test the interactive_menu with input 'QUIT' to simulate exit.
        """
        choice = interactive_menu(self.config_default)
        self.assertEqual(choice, "QUIT")
        output = strip_ansi_codes(mock_stdout.getvalue())
        self.assertIn("Generate:", output)

    @patch("builtins.input", return_value="EXIT")
    @patch("sys.stdout", new_callable=StringIO)
    def test_input_exit(self, mock_stdout, mock_input):
        """
        Test the interactive_menu with input 'EXIT' to simulate exit.
        """
        choice = interactive_menu(self.config_default)
        self.assertEqual(choice, "EXIT")
        output = strip_ansi_codes(mock_stdout.getvalue())
        self.assertIn("Generate:", output)

    @patch("builtins.input", return_value="   ")
    @patch("sys.stdout", new_callable=StringIO)
    def test_input_only_whitespace(self, mock_stdout, mock_input):
        """
        Test the interactive_menu with input that is only whitespace.
        """
        choice = interactive_menu(self.config_default)
        self.assertEqual(choice, "")
        output = strip_ansi_codes(mock_stdout.getvalue())
        self.assertIn("press Enter to exit", output)

    @patch("builtins.input", side_effect=KeyboardInterrupt)
    @patch("sys.stdout", new_callable=StringIO)
    def test_keyboard_interrupt(self, mock_stdout, mock_input):
        """
        Test the interactive_menu handles KeyboardInterrupt (Ctrl+C).
        """
        with self.assertRaises(KeyboardInterrupt):
            interactive_menu(self.config_default)
        output = strip_ansi_codes(mock_stdout.getvalue())
        self.assertIn("Generate:", output)

if __name__ == "__main__":
    unittest.main()
