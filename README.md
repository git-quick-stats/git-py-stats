# Git Py Stats

Git Py Stats is a Python-based fork inspired by [git-quick-stats](https://github.com/arzzen/git-quick-stats).
It offers a similar set of git statistics and reports, but it's built entirely
using Python 3, providing improved cross-platform compatibility
and ease of maintenance.

## Why Git Py Stats?

While `git-quick-stats` is a fantastic tool, it has some limitations due to its
reliance on Bash and external utilities:

- **Cross-Platform Compatibility**: `git-quick-stats` can have issues running
 on different platforms. For example, macOS requires GNU versions of certain
 utilities for proper functionality.
- **Dependency on External Tools**: Although it is written in Bash, it depends
 heavily on external tools like `awk`, `sed`, and `grep`,
 which may not be available or behave subtly different across systems.
- **Robust File Generation**: `git-quick-stats` has the ability to export
 stats in JSON and CSV format, but they are home-grown implementations.
- **Difficult to Test and Extend**: Bash scripts are inherently harder to test
 and extend compared to a Python-based solution.

Git Py Stats addresses these issues by leveraging Python's standard library,
ensuring that it pulls in code tested by the Python team and works seamlessly
on any platform with Python 3 installed. Its goal still maintains the spirit
of `git-quick-stats` in that it will never require anything outside of
Python 3 and git.

## Features

Git Py Stats aims to maintain feature parity with the original `git-quick-stats`:

- Contribution stats by author
- Git changelogs and stats by branch or author
- Commits analysis by date, month, year, weekday, and hour
- Branch history and contributor analysis
- Suggested code reviewers based on commit history
- CSV and JSON output for various statistics

and more in both interactive and non-interactive modes.

## Missing Features

Git Py Stats is currently in beta format. As such, it is missing the following:

- Git log since and until functionality
- Git log limit functionality
- Git log options functionality
- Git pathspec functionality
- Git merge view strategies
- Git branch adjustability to customize what branch you're on
- Color themes
- Linux package installs (only installable via `pip` and locally currently)
- macOS package installs
- Lacks a Docker image

## Requirements

- **Python 3.x**: Git Py Stats requires Python 3.x installed on your system.
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

3. **Verify the Installation**:

    ```bash
    git-py-stats --help
    ```

### Using `setup.py`

If you prefer using `setup.py` directly:

1. **Install the Package**:

    ```bash
    python setup.py install
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

## Development

- **`src/git_py_stats`**: Core package containing main functionality
- **`tests`**: Contains test cases for the various modules

### Running Tests

1. **Install Testing Dependencies**:

    ```bash
    pip install -r requirements-dev.txt
    ```

2. **Run Tests**:

    ```bash
    pytest tests/
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

## License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for more details.

## Author

Tom Ice

