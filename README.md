# Git Py Stats

<div align="center">
  
[![CI](https://github.com/tomice/git-py-stats/workflows/CI/badge.svg)](https://github.com/tomice/git-py-stats/actions)
[![codecov](https://codecov.io/gh/tomice/git-py-stats/branch/main/graph/badge.svg)](https://codecov.io/gh/tomice/git-py-stats)
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

![mainMenuScreenshot](https://github.com/user-attachments/assets/db99d110-c43b-4ba7-baa9-b7d0167475cf)

## Table of Contents

- [Why Git Py Stats?](#why-git-py-stats)
- [Features](#features)
  - [Changes from Original](#changes-from-original)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Using PyPI](#using-pypi)
  - [Using `setup.py`](#using-setuppy)
  - [From Source](#from-source)
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
  - [Sorting Contribution Stats](#sorting-contribution-stats)
  - [Commit Days](#commit-days)
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
  installed depending on how the user's system is configured, especially if you
  happen to be running this on a minimal Linux distro targeted for embedded
  devices with a sparse dev environment.
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
    python --version
    ```

  If your `python` is symlinked to Python 2, you can use
  [`pyenv`](https://github.com/pyenv/pyenv) to switch between Python versions.
  Alternatively, as long as Python 3 is installed, you should be able to replace
  any of the `python` commands with `python3`.

- **Git**:
  Git should be installed and available in your system's `PATH`.

## Installation

### Using PyPI

1. **Install Using pip**:

    ```bash
    pip install git-py-stats
    ```

    That's it! You can now use `git-py-stats` anywhere on your system
    while inside of a git repo!

    If you experience conflicts with other packages,
    try using [`venv`](https://docs.python.org/3/library/venv.html)

### Using `setup.py`

If you prefer using `setup.py` directly:

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/tomice/git-py-stats.git
    cd git-py-stats
    ```

2. **Install the Package**:

    ```bash
    python setup.py install
    ```

    That's it! You can now use `git-py-stats` anywhere on your system
    while inside of a git repo! If you don't have admin permissions,
    you can use the `--user` flag at the end of the command to install
    this locally.

### From Source

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/tomice/git-py-stats.git
    cd git-py-stats
    ```

2. **Set PYTHONPATH**:

    Set the root of `git-py-stats` to be prefixed to your `PYTHONPATH`:

    ```bash
    export PYTHONPATH=$(pwd):$PYTHONPATH
    ```

    That's it! You can now use `git-py-stats` anywhere on your system
    while inside of a git repo, albeit with a slight modification.
    Commands will need to be done in the following manner:

    ```bash
    python -m git_py_stats.main --help
    ```

    This will tell Python to run the `git_py_stats.main` module directly.
    This method is usually best for devs who want to help contribute to the
    project without going through the install process a normal end user would.

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
Works with command `--csv-output-by-branch` only currently.

```bash
export _GIT_BRANCH="master"
```

### Ignore Authors

You can set the variable `_GIT_IGNORE_AUTHORS` to filter out specific
authors. It will currently work with the "Code reviewers", "New contributors",
"All branches", and "Output daily stats by branch in CSV format" options.

```bash
export _GIT_IGNORE_AUTHORS="(author@examle.com|username)"
```

### Sorting Contribution Stats

You can sort contribution stats by field `name`, `commits`, `insertions`,
`deletions`, or `lines` (total lines changed), followed by a hyphen and
a direction (`asc`, `desc`).

```bash
export _GIT_SORT_BY="name-asc"
or
export _GIT_SORT_BY="lines-desc"
or
export _GIT_SORT_BY="deletions-asc"
```

### Commit Days

You can set the variable `_GIT_DAYS` to set the number of days for the heatmap.

```bash
export _GIT_DAYS=30
```

### Color Themes

You can change to the legacy color scheme by toggling the variable `_MENU_THEME`
between `default` and `legacy`. You can completely disable the color theme by
setting the `_MENU_THEME` variable to `none`.

```bash
export _MENU_THEME="legacy"
# or
export _MENU_THEME="none"
```

## Contributing

We welcome contributions of all kinds! Please read our
[CONTRIBUTING.md](https://github.com/tomice/git-py-stats/blob/main/CONTRIBUTING.md)
guide to learn how to get involved. It contains more detailed information to
help walk you through how to contribute. If there are any questions, feel free
to ask when submitting your issue or PR, and one of the maintainers will help!

To sum it up, please do the following:

1. Create an [issue](https://github.com/git-quick-stats/git-py-stats/issues/new) on GitHub.
2. Clone the [repo](https://github.com/git-quick-stats/git-py-stats) and make your changes.
3. Write the accompanying [tests](https://docs.python.org/3/library/unittest.html).
4. Auto lint with [`ruff`](https://github.com/astral-sh/ruff).
5. Auto format with [`black`](https://github.com/psf/black).
6. Submit the [PR](https://github.com/git-quick-stats/git-py-stats/compare).

## Code of Conduct

To ensure a positive and inclusive community, please follow our
[Code of Conduct](https://github.com/tomice/git-py-stats/blob/main/CODE_OF_CONDUCT.md)
during your interactions.

## License

This project is licensed under the MIT License.
See the [LICENSE](https://github.com/tomice/git-py-stats/blob/main/LICENSE)
file for more details.

## Author

Tom Ice
