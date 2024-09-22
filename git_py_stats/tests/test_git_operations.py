import unittest

from git_py_stats.git_operations import run_git_command, check_git_repository

class TestGitOperations(unittest.TestCase):
    """
    Unit test class for testing git_operations.
    """

    def test_run_git_command(self) -> None:
        """
        Test case for the run_git_command function.

        Checks if `run_git_command` executes a basic git command (`git --version`)
        and returns a non-None value, which indicates that the command was successful.
        The function is expected to return the output of the command as a string.

        The test might fail if git is not installed or if the command path is not
        correctly set.
        """
        
        self.assertIsNotNone(run_git_command(['git', '--version']))

    def test_check_git_repository(self) -> None:
        """
        Test case for the check_git_repository function.

        Checks if `check_git_repository` correctly identifies whether the current
        directory is a git repo. The function is expected to return a boolean
        value (`True` if the directory is a git repository, `False` otherwise).

        This test's result will depend on the context of the directory in which
        the test is run. We should only run this test in a known git repository for
        predictable results.
        """
        
        self.assertIsInstance(check_git_repository(), bool)

if __name__ == '__main__':
    unittest.main()

