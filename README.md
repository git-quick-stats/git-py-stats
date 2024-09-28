# Git Py Stats

<div align="center">
  
[![CI](https://github.com/tomice/git-py-stats/workflows/CI/badge.svg)](https://github.com/tomice/git-py-stats/actions)
[![Ruff](https://img.shields.io/badge/linting-Ruff-green?logo=ruff)](https://docs.astral.sh/ruff/)
[![Black](https://img.shields.io/badge/code%20style-Black-000000.svg?logo=black)](https://black.readthedocs.io/en/stable/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/tomice/git-py-stats)](https://github.com/tomice/git-py-stats/issues)
[![GitHub stars](https://img.shields.io/github/stars/tomice/git-py-stats?style=social)](https://github.com/tomice/git-py-stats/stargazers)
[![Contributors](https://img.shields.io/github/contributors/tomice/git-py-stats)](https://github.com/tomice/git-py-stats/graphs/contributors)
[![Python Versions](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)

</div>

Git Py Stats is a Python-based fork inspired by [git-quick-stats](https://github.com/arzzen/git-quick-stats).
It offers a similar set of git statistics and reports, but it's built entirely
using Python 3, providing improved cross-platform compatibility
and ease of maintenance.

![mainMenuScreenshot](https://github.com/user-attachments/assets/4c3f49d8-62a9-4208-a968-5270e36aa3b8)

## Table of Contents

- [Why Git Py Stats?](#why-git-py-stats)
- [Features](#features)
  - [Changes from Original](#changes-from-original)
- [Requirements](#requirements)
- [Installation](#installation)
  - [From Source](#from-source)
  - [Using `setup.py`](#using-setuppy)
- [Usage](#usage)
  - [Interactive Mode](#interactive-mode)
  - [Non-Interactive Mode](#non-interactive-mode)
- [Advanced Usage](#advanced-usage)
  - [Git Log Since and Until](#git-log-since-and-until)
  - [Git Log Limit](#git-log-limit)
  - [Git Log Options](#git-log-options)
  - [Git Pathspec](#git-pathspec)
  - [Git Merge View Strategy](#git-merge-view-strategy)
  - [Git Branch](#git-branch)
  - [Color Themes](#color-themes)
- [Contributing](#contributing)
- [Code of Conduct](#code-of-conduct)
- [License](#license)
- [Author](#author)

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

Git Py Stats aims to maintain feature parity with `git-quick-stats` with
features such as:

- Contribution stats by author
- Git changelogs and stats by branch or author
- Commits analysis by date, month, year, weekday, and hour
- Branch history and contributor analysis
- Suggested code reviewers based on commit history
- CSV and JSON output for various statistics

and more in both interactive and non-interactive modes.

### Changes from Original

While this project aims to be feature-complete and 1:1 with `git-quick-stats`,
there may be instances where this version differs from the base project.
The following is a list of differences that this project will maintain compared
to the parent project:

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

- **Python 3.8+**:
  Git Py Stats requires Python 3.8 or higher installed on your system.
  While it may work with older versions, there is no guarantee as it is
  currently untested with versions below 3.8.
  You can check your Python version with:

    ```bash
    python3 --version
    ```

- **Git**:
  Git should be installed and available in your system's `PATH`.

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

## Advanced Usage

It is possible for `git-py-stats` to read shell environment variables just like
`git-quick-stats` does. As it aims to maintain 1:1 compatibility, all of the
same arguments work the same as the parent project.

### Git Log Since and Until

You can set the variables `_GIT_SINCE` and/or `_GIT_UNTIL` before running
`git-py-stats` to limit the git log.
These work similar to git's built-in `--since` and `--until` log options.

```bash
export _GIT_SINCE="2017-01-20"
export _GIT_UNTIL="2017-01-22"
```

Once set, run `git-py-stats` as normal. Note that this affects all stats that
parse the git log history until unset.

### Git Log Limit

You can set variable `_GIT_LIMIT` for limited output.
It will affect the "changelogs" and "branch tree" options.
The default limit is `10`.

```bash
export _GIT_LIMIT=20
```

### Git Log Options

You can set `_GIT_LOG_OPTIONS` for
[git log options](https://git-scm.com/docs/git-log#_options):

```bash
export _GIT_LOG_OPTIONS="--ignore-all-space --ignore-blank-lines"
```

### Git Pathspec

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

### Git Merge View Strategy

You can set the variable `_GIT_MERGE_VIEW` to enable merge commits to be part
of the stats by setting `_GIT_MERGE_VIEW` to `enable`. You can also choose to
only show merge commits by setting `_GIT_MERGE_VIEW` to `exclusive`.
Default is to not show merge commits.
These work similar to git's built-in `--merges` and `--no-merges` log options.

```bash
export _GIT_MERGE_VIEW="enable"
export _GIT_MERGE_VIEW="exclusive"
```

### Git Branch

You can set the variable `_GIT_BRANCH` to set the branch of the stats.
Works with commands `--git-stats-by-branch` and `--csv-output-by-branch`.

```bash
export _GIT_BRANCH="master"
```

### Color Themes

You can change to the legacy color scheme by toggling the variable
`_MENU_THEME` between `default` and `legacy`

```bash
export _MENU_THEME="legacy"
```

## Contributing

We welcome contributions of all kinds! Please read our
[CONTRIBUTING.md](CONTRIBUTING.md) guide to learn how to get involved.

## Code of Conduct

To ensure a positive and inclusive community, please follow our
[Code of Conduct](CODE_OF_CONDUCT.md) during your interactions.

## License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for more details.

## Author

Tom Ice
