# Contributing to Git Py Stats

Thank you for your interest in contributing to **Git Py Stats**!
We welcome contributions of all kinds, including bug reports, feature requests,
documentation improvements, and code enhancements.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
  - [Reporting Issues](#reporting-issues)
  - [Suggesting Features](#suggesting-features)
  - [Submitting Pull Requests](#submitting-pull-requests)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
  - [Running Tests](#running-tests)
  - [Additional Tips](#additional-tips)
- [Style Guidelines](#style-guidelines)
- [Acknowledgments](#acknowledgments)

## Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) to understand the
expectations for participation in this project.

## How to Contribute

### Reporting Issues

If you encounter any bugs or have suggestions for improvements,
please [open an issue](https://github.com/tomice/git-py-stats/issues).
When reporting an issue, please include the following:

- A clear and descriptive title.
- A detailed description of the problem or suggestion.
- Steps to reproduce the issue (if applicable).
- Any relevant screenshots or error messages.

### Suggesting Features

Have an idea for a new feature? We'd love to hear it! Please create an issue
with the tag `feature request` and provide as much detail as possible about
the proposed functionality.

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

5. **Commit Your Changes**

   Write clear and descriptive commit messages.

   ```bash
   git commit -m "Add feature: description of your feature"
   ```

6. **Push to Your Fork**

   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**

   Navigate to the original repository and click on "New Pull Request".
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
- **Naming Conventions**:
  Use clear and descriptive names for variables, functions, and classes.
  When in doubt, always try to follow [PEP 8](https://pep8.org/).
- **Documentation**:
  Include docstrings for all public modules, functions, classes, and methods.
  Also include type hints for functions, classes, and methods.

While not strict, try to keep documentation around 80 columns per line.

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
    python3 -m unittest discover -s git_py_stats/tests
    ```

3. **Run a Specific Test File**:

    To run a specific test file, you can use:

    ```bash
    python3 -m unittest git_py_stats.tests.test_generate_cmds
    ```

### Additional Tips

- Ensure that all test files follow the naming convention `test_*.py`.
- To view more detailed output, use the `-v` (verbose) flag:

    ```bash
    python3 -m unittest discover -s git_py_stats/tests -v
    ```

- To run all tests automatically and display a summary of results:

    ```bash
    python3 -m unittest discover -s git_py_stats/tests
    ```

- If you need help writing tests, here are tutorials and books that might help:
  - [Python's unittest docs](https://docs.python.org/3/library/unittest.html)
  - [Python's unittest.mock docs](https://docs.python.org/3/library/unittest.mock.html)
  - [Obey the Testing Goat](https://www.obeythetestinggoat.com/pages/book.html#toc)

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
