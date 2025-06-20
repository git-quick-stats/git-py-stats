# Contributing to Git Py Stats

Thank you for your interest in contributing to **Git Py Stats**!
We welcome contributions of all kinds, including bug reports, feature requests,
documentation improvements, and code enhancements.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
  - [Requirements](#requirements)
  - [Reporting Issues](#reporting-issues)
  - [Suggesting Features](#suggesting-features)
  - [Submitting Pull Requests](#submitting-pull-requests)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
  - [Running Tests](#running-tests)
  - [Additional Tips](#additional-tips)
- [Linting](#linting)
- [Auto Formatting](#auto-formatting)
- [Style Guidelines](#style-guidelines)
- [Acknowledgments](#acknowledgments)

## Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) to understand the
expectations for participation in this project.

## How to Contribute

### Requirements

Contributing is meant to be as painless as possible. However, for the
sake of a nicely readable and unified codebase, there are some extra
steps needed before anybody can contribute. While the actual application
itself only requires Python 3 and Git, contributing will require you to
install additional applications. The following are required in order to
pass our CI builder:

- [`ruff`](https://github.com/astral-sh/ruff)
- [`black`](https://github.com/psf/black)

We understand these opinionated tools may be a bit controversial,
but these tools help keep consistency and maintain some semblance
of standardization across the codebase. If you code does not pass the
CI builder, it will not be allowed to be merged in, so please keep that
in mind when submitting code.

### Reporting Issues

If you encounter any bugs or have suggestions for improvements,
please [open an issue](https://github.com/git-quick-stats/git-py-stats/issues).
We recommend opening up an issue regardless of how minor the change
may be, as it allows us to better track changes in the project.
You can even submit a pull request immediately after to address the issue.

When reporting an issue, please try to include the following:

- A clear and descriptive title.
- A detailed description of the problem or suggestion.
- Steps to reproduce the issue (if applicable).
- Any relevant screenshots or error messages.

### Suggesting Features

Have an idea for a new feature? We'd love to hear it! Please create an issue
with the tag `feature request` and provide as much detail as possible about
the proposed functionality. One of the maintainers should get back to you
within a timely manner to discuss the new features.

Please note that this project strives to maintain feature parity with the
parent project, [`git-quick-stats`](https://github.com/git-quick-stats/git-quick-stats/).
Depending on the change, we may ask you to first submit the feature request
to the parent project before we adopt it.

### Submitting Pull Requests

Contributions are made via pull requests. Here's how to submit one:

1. **Fork the Repository**

   Click the "Fork" button at the top right of this repository page to
   create your own fork.

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/your-username/git-py-stats.git
   cd git-py-stats
   ```

3. **Create a New Branch**

   It's best to create a new branch for each significant change.

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**

   - Try to follow the [PEP 8](https://pep8.org/) style guide.
   - Add or update tests as necessary.
   - Update documentation if your changes require it.
   - Run [Ruff](https://docs.astral.sh/ruff/)
   - Run [Black](https://pypi.org/project/black/)

5. **Commit Your Changes**

   Write clear and descriptive commit messages.

   ```bash
   git commit -m "Add feature: description of your feature"
   ```

   Please note that GitHub has [built-in keywords](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue)
   that allow you to automatically link an issue to a commit message.
   Making use of these makes it easier to see exactly what each
   commit is attempting to address.

7. **Push to Your Fork**

   ```bash
   git push origin feature/your-feature-name
   ```

8. **Open a Pull Request**

   Navigate to the original repository and click on "New Pull Request",
   or try [this link](https://github.com/git-quick-stats/git-py-stats/compare).
   Provide a clear description of your changes and reference any related issues
   should they exist.

## Coding Standards

- **Language**:
  We currently have a minimum requirement of Python 3.8. While this code may
  work on Python 3 versions below that, it is not guaranteed.
- **Dependencies**:
  Git Py Stats should not have any dependencies outside of Python 3 and `git`.
  That means nobody should ever have to type in `pip foo` before being able to
  run this program.
- **Style Guide**:
  We use [Black](https://pypi.org/project/black/) for auto formatting code in
  the repo before it gets merged for style consistency.
  We also use [Ruff](https://docs.astral.sh/ruff/) for linting in the repo
  before it gets merged for improving code quality.
- **Naming Conventions**:
  Use clear and descriptive names for variables, functions, and classes.
  When in doubt, always try to follow [PEP 8](https://pep8.org/).
- **Documentation**:
  Include docstrings for all public modules, functions, classes, and methods.
  Also include type hints for functions, classes, and methods.

While not strict, try to keep documentation around 80 columns per line.
There is a hard limit of 100 columns per line of code currently.

## Testing

This project uses Python's built-in
[unittest](https://docs.python.org/3/library/unittest.html) testing framework.
Ensure that all tests pass before submitting a pull request.

### Running Tests

1. **Navigate to the Project Directory**:

    ```bash
    cd git-py-stats
    ```

2. **Run All Tests**:

    You can run all tests using the `unittest` discovery mode, which will
    automatically find and execute all test files named `test_*.py`
    within the `git_py_stats/tests/` directory:

    ```bash
    python -m unittest discover -s git_py_stats/tests
    ```

3. **Run a Specific Test File**:

    To run a specific test file, you can use:

    ```bash
    python -m unittest git_py_stats.tests.test_generate_cmds
    ```

### Additional Tips

- Ensure that all test files follow the naming convention `test_*.py`.
- To view more detailed output, use the `-v` (verbose) flag:

    ```bash
    python -m unittest discover -s git_py_stats/tests -v
    ```

- To run all tests automatically and display a summary of results:

    ```bash
    python -m unittest discover -s git_py_stats/tests
    ```

- If you need help writing tests, here are tutorials and books that might help:
  - [Python's unittest docs](https://docs.python.org/3/library/unittest.html)
  - [Python's unittest.mock docs](https://docs.python.org/3/library/unittest.mock.html)
  - [Obey the Testing Goat](https://www.obeythetestinggoat.com/pages/book.html#toc)

## Linting

As stated before, we use `ruff` for linting. Installing `ruff` will depend on
your system and how you want to manage your dependencies in general. Ubuntu
and Fedora can use [snaps](https://snapcraft.io/install/ruff/ubuntu),
Arch can use [pacman](https://archlinux.org/packages/extra/x86_64/ruff/),
and of course, anybody can use [PyPI](https://pypi.org/project/ruff/).

Ultimately, it is up to you how you wish to install `ruff`, but it is required
to pass in order to be able to get past our CI builder.

Once `ruff` is installed, you can invoke it by running the following command
inside the `git-py-stats` repo:

```sh
ruff check git_py_stats
```

If it passes, `ruff` will print out "All checks passed!" If it gives an
error, it will point you to where the issue is and mention the problem.

Sometimes, minor issues can be fixed using the `--fix` flag. `ruff` will
try to point these out and fix them for you. Feel free to use this option,
but realize it might conflict with `black`, so always try to run the linter
and get that to pass before running it through the auto formatter.

## Auto Formatting

Like earlier, we are opinionated on how the code should look. As such, we
have a highly opinionated auto formatter thanks to `black`. Just like with
`ruff`, installing `black` will depend on your system and how you want to
manage dependencies. You can see how to install it on a slew of different
operating systems [here](https://snapcraft.io/black). Like nearly all Python
projects, there is also a [PyPI](https://pypi.org/project/black/) equivalent.

Install this however you wish, but your code must pass `black`'s default
auto formatter settings in order to be able to pass our CI builder.

Once `black` is installed, you can invoke it by running the following command
inside the `git-py-stats` repo:

```sh
black .
```

It should report back something similar to the following:

```sh
All done! ✨ 🍰 ✨
21 files left unchanged.
```

That's it! If there were any changes, commit them. Do *not* try to re-adjust
anything as that might break the auto formatting you just applied.

Once that's done, your code is finally ready for a pull request!

## Style Guidelines

- Write clear and concise code.
- Avoid unnecessary complexity.
- Ensure that your code is readable and maintainable.
- Comment your code where necessary to explain complex logic.

## Acknowledgments

- Thanks to each and every one of the contributors of
  [git-quick-stats](https://github.com/arzzen/git-quick-stats) for inspiring
  this project. Without them, this project would not exist.
- Special thanks to all the contributors who help make Git Py Stats better!
