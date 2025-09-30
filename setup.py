from setuptools import setup, find_packages

# Read the long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="git-py-stats",
    version="0.2.0",
    packages=find_packages(exclude=("git_py_stats.tests", "git_py_stats.tests.*")),
    entry_points={
        "console_scripts": [
            "git-py-stats=git_py_stats.main:main",
        ],
    },
    data_files=[
        ("share/man/man1", ["man/git-py-stats.1"]),
    ],
    description="A Python Implementation of git-quick-stats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tom Ice",
    author_email="contact@thomasice.com",
    license="MIT",
    url="https://github.com/git-quick-stats/git-py-stats",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    keywords="git stats statistics command-line",
)
