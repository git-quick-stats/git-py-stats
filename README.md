
# Git Py Stats

Git Py Stats is a Python-based fork inspired by [git-quick-stats](https://github.com/arzzen/git-quick-stats).
It offers a similar set of git statistics and reports, but it's built entirely
using Python 3, providing improved cross-platform compatibility
and ease of maintenance.

![mainMenuScreenshot](https://github.com/user-attachments/assets/4c3f49d8-62a9-4208-a968-5270e36aa3b8)

## Why Git Py Stats?

While `git-quick-stats` is a fantastic tool, it has some limitations due to its
reliance on Bash and external utilities:

- **Cross-Platform Compatibility**: `git-quick-stats` can have issues running
  on different platforms. For example, macOS requires GNU versions of certain
  utilities for proper functionality, and the Windows version either requires
  WSL or Cygwin to run.
- **Dependency on External Tools**: Although it is written in Bash, it depends
  heavily on external tools like `tput`, `column`, and `grep`, which may not be
  installed depending on how the user's system is configured.
- **Robust File Generation**: `git-quick-stats` has the ability to export
  stats in JSON and CSV format, but they are home-grown implementations that
  are currently in experimental mode.
- **Difficult to Test and Extend**: Bash scripts are inherently harder to test
  and extend compared to a Python-based solution that can leverage
  [unittest](https://docs.python.org/3/library/unittest.html).

Git Py Stats tackles these challenges by leveraging Python's standard library,
guaranteeing that it incorporates code vetted by the Python team and operates
smoothly on any platform with Python 3 installed. It stays true to the essence
of `git-quick-stats` by ensuring that no dependencies beyond Python 3 and `git`
are ever required.

## Features

Git Py Stats aims to maintain feature parity with the original `git-quick-stats`:

- Contribution stats by author
- Git changelogs and stats by branch or author
- Commits analysis by date, month, year, weekday, and hour
- Branch history and contributor analysis
- Suggested code reviewers based on commit history
- CSV and JSON output for various statistics

and more in both interactive and non-interactive modes.

## Feature Comparison

The following is a list of features that compares `git-py-stats` development
with the capabilities `git-quick-stats` currently has. Completed means there
exists essentially 1:1 functionality between the two projects. Stubbed means
`git-py-stats` has the feature available, but it might not match the original
project's version. Not Yet Implemented means it does not exist yet:

| Feature                                         | Status                 | Description                                             |
|-------------------------------------------------|------------------------|---------------------------------------------------------|
| **UI**                                          | Completed ✔️            | General UI when launching interactive mode              |
| **Interactive Mode**                            | Completed ✔️            | Enables interactive sessions for user inputs.           |
| **Non-interactive Mode**                        | Completed ✔️            | Allows usage without interactive prompts.               |
| **Contribution Stats**                          | Completed ✔️            | Displays overall contribution statistics.               |
| **Contribution Stats by Author**                | Completed ✔️            | Shows contribution stats by individual authors.         |
| **Changelogs**                                  | Completed ✔️            | Lists commit logs over 10 last days of commits.         |
| **Changelogs by Author**                        | Completed ✔️            | Filters changelogs based on the author.                 |
| **Code Reviewers**                              | Completed ✔️            | Identifies code reviewers based on contribution.        |
| **My Daily Stats**                              | Completed ✔️            | Tracks daily statistics customized for the user.        |
| **Output Daily Stats by Branch in CSV**         | Completed ✔️            | Exports daily branch stats in CSV format.               |
| **Save Git Log Output in JSON Format**          | Completed ✔️            | Stores git logs in JSON.                                |
| **Branch Tree View**                            | Completed ✔️            | Visual representation of the branch hierarchy.          |
| **All Branches (Sorted by Most Recent Commit)** | Completed ✔️            | Lists all branches ordered by latest commit date.       |
| **All Contributors (Sorted by Name)**           | Completed ✔️            | Displays all contributors sorted alphabetically.        |
| **New Contributors (Sorted by Email)**          | Completed ✔️            | Lists new contributors sorted by their email addresses. |
| **Git Commits per Author**                      | Completed ✔️            | Counts commits made by each author.                     |
| **Git Commits per Date**                        | Completed ✔️            | Counts commits based on the date.                       |
| **Git Commits per Month**                       | Completed ✔️            | Counts commits based on the monthly.                    |
| **Git Commits per Year**                        | Completed ✔️            | Counts commits based on the year.                       |
| **Git Commits per Weekday**                     | Completed ✔️            | Counts commits based on the weekday.                    |
| **Git Commits per Weekday by Author**           | Completed ✔️            | Shows weekday commit counts by given author.            |
| **Git Commits per Hour**                        | Completed ✔️            | Counts commits based on the hour.                       |
| **Git Commits per Hour by Author**              | Completed ✔️            | Shows hourly commit count hour by given author.         |
| **Git Commits per Timezone**                    | Completed ✔️            | Counts commits based on timezones.                      |
| **Git Commits per Timezone by Author**          | Completed ✔️            | Shows timezone-based commit counts by given author.     |
| **Since Variable Adjustable by User**           | Completed ✔️            | Allows users to set the starting point for commit logs. |
| **Until Variable Adjustable by User**           | Completed ✔️            | Enables users to define the end point for commit logs.  |
| **Pathspec Variable Adjustable by User**        | Completed ✔️            | Filters commits based on specified path patterns.       |
| **Merge View Variable Adjustable by User**      | Completed ✔️            | Controls the inclusion of merge commits in views.       |
| **Limit Variable Adjustable by User**           | Completed ✔️            | Sets the maximum number of commits to display.          |
| **Log Options Variable Adjustable by User**     | Completed ✔️            | Customizes git log command options.                     |
| **Legacy Theme**                                | Completed ✔️            | Restores the previous visual theme of the application.  |
| **Linux Package Install**                       | Not Yet Implemented ❌ | Allows Linux users to install via a package manager.    |
| **macOS Package install**                       | Not Yet Implemented ❌ | Allows macOS users to install via brew.                 |
| **Docker Development Image**                    | Completed ✔️            | Provides a Docker development image for CI/CD.          |

## Changes from Original

While this project aims to be feature-complete and 1:1 with the `git-quick-stats`,
there may be instances where this version differs from the base project by design.
The following is a list of differences that this project will maintain compared to
the parent project:

- Author, dates, and branch names can be passed via cmdline without interaction
  by the user. This means you can now do `git-py-stats -L "John Doe"` instead
  of being prompted to enter the name after executing the non-interactive cmd.
- CSV output is now saved to a file instead of printing out to the terminal.
  This file will be saved to wherever the process was executed. The name will
  be `git_daily_stats.csv`
- JSON output is saved to a file wherever the process was executed instead of
  one that is provided by the user. The name will be `git_log.json`
- JSON and CSV formatting has changed slightly from the original.
- The New Contributors function shows the user's name next to the email in case
  no known mailmap has been implemented for that user.

## Requirements

- **Python 3.6+**: Git Py Stats requires Python 3.6 or higher installed on your system.
  You can check your Python version with:

    ```bash
    python3 --version
    ```

- **Git**: Git should be installed and available in your system's PATH.

## Installation

### From Source

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/tomice/git-py-stats.git
    cd git-py-stats
    ```

2. **Install the Package**:

    You can install the package locally in editable mode.
    This allows you to run `git-py-stats` from anywhere on your system.

    ```bash
    pip install -e .
    ```

    Or you can run it locally without `pip` by doing the following
    while inside the `git-py-stats` repo from Step 1:

    ```bash
    export PYTHONPATH=$(pwd):$PYTHONPATH
    ```

3. **Verify the Installation**:

    While inside of a valid git repo, type the following:

    ```bash
    git-py-stats --help
    ```

    If you decided to use the `PYTHONPATH` method, commands will need
    to be done in the following manner:

    ```bash
    python3 -m git_py_stats.main --help
    ```

### Using `setup.py`

If you prefer using `setup.py` directly:

1. **Install the Package**:

    ```bash
    python3 setup.py install
    ```

2. **Verify the Installation**:

    ```bash
    git-py-stats --help
    ```

## Usage

You can run Git Py Stats in both interactive and non-interactive modes:

### Interactive Mode

Simply run the tool without any arguments to enter the interactive menu:

```bash
git-py-stats
```

### Non-Interactive Mode

Run the tool with specific command-line options for direct output. For example:

- **Detailed Git Stats**:

    ```bash
    git-py-stats -T
    ```

- **Git Stats by Branch**:

    ```bash
    git-py-stats -R master
    ```

- **List Contributors**:

    ```bash
    git-py-stats -C
    ```

For a full list of available options, run:

```bash
git-py-stats --help
```

### Advanced Usage

It is possible for `git-py-stats` to read shell environment variables just like
`git-quick-stats` does. As it aims to maintain 1:1 compatibility, all of the
same arguments work the same as the parent project.

#### Git log since and until

You can set the variables `_GIT_SINCE` and/or `_GIT_UNTIL` before running
`git-py-stats` to limit the git log.
These work similar to git's built-in `--since` and `--until` log options.

```bash
export _GIT_SINCE="2017-01-20"
export _GIT_UNTIL="2017-01-22"
```

Once set, run `git-py-stats` as normal. Note that this affects all stats that
parse the git log history until unset.

#### Git log limit

You can set variable `_GIT_LIMIT` for limited output.
It will affect the "changelogs" and "branch tree" options.
The default limit is `10`.

```bash
export _GIT_LIMIT=20
```

#### Git log options

You can set `_GIT_LOG_OPTIONS` for
[git log options](https://git-scm.com/docs/git-log#_options):

```bash
export _GIT_LOG_OPTIONS="--ignore-all-space --ignore-blank-lines"
```

#### Git pathspec

You can exclude a directory from the stats by using
[pathspec](https://git-scm.com/docs/gitglossary#gitglossary-aiddefpathspecapathspec).

```bash
export _GIT_PATHSPEC=':!directory'
```

You can also exclude files from the stats.
Note that it works with any alphanumeric, glob, or regex that git respects.

```bash
export _GIT_PATHSPEC=':!package-lock.json'
```

#### Git merge view strategy

You can set the variable `_GIT_MERGE_VIEW` to enable merge commits to be part
of the stats by setting `_GIT_MERGE_VIEW` to `enable`. You can also choose to
only show merge commits by setting `_GIT_MERGE_VIEW` to `exclusive`.
Default is to not show merge commits.
These work similar to git's built-in `--merges` and `--no-merges` log options.

```bash
export _GIT_MERGE_VIEW="enable"
export _GIT_MERGE_VIEW="exclusive"
```

#### Git branch

You can set the variable `_GIT_BRANCH` to set the branch of the stats.
Works with commands `--git-stats-by-branch` and `--csv-output-by-branch`.

```bash
export _GIT_BRANCH="master"
```

#### Color themes

You can change to the legacy color scheme by toggling the variable
`_MENU_THEME` between `default` and `legacy`

```bash
export _MENU_THEME="legacy"
```

## Development

This section is currently under development and is changing rapidly as we work
on getting features added. The current structure is as follows:

- **`git_py_stats/`**: Core package
- **`git_py_stats/tests/`**: Test cases for the various modules

### Code Formatting

This project uses [Black](https://black.readthedocs.io/en/stable/) for code formatting.
To ensure consistency, please try to autoformat your code with one of the various
cool autoformatters out there before submitting a PR.

Here is how to format all Python code with Black before submitting changes:

```bash
pip install black
cd git-py-stats
black .
```

- For more information about Black, refer to the [official documentation](https://black.readthedocs.io/en/stable/).

### Testing

This project uses Python's built-in `unittest` framework for testing.

#### Running Tests

1. **Navigate to the Project Directory**:

    ```bash
    cd git-py-stats
    ```

2. **Run All Tests**:

    You can run all tests using the `unittest` discovery mode, which will
    automatically find and execute all test files named `test_*.py`
    within the `git_py_stats/tests/` directory:

    ```bash
    python3 -m unittest discover -s git_py_stats/tests
    ```

3. **Run a Specific Test File**:

    To run a specific test file, you can use:

    ```bash
    python3 -m unittest git_py_stats.tests.test_generate_cmds
    ```

#### Additional Tips

- Ensure that all test files follow the naming convention `test_*.py`.
- To view more detailed output, use the `-v` (verbose) flag:

    ```bash
    python3 -m unittest discover -s git_py_stats/tests -v
    ```

- To run all tests automatically and display a summary of results:

    ```bash
    python3 -m unittest discover -s git_py_stats/tests
    ```

## Contribution

Contributions are welcome! If you encounter a bug or have a feature request,
please [open an issue](https://github.com/tomice/git-py-stats/issues).

To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

Please try to adhere to [PEP 8](https://peps.python.org/pep-0008/).

## License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for more details.

## Author

Tom Ice
