from setuptools import setup, find_packages

setup(
    name='git-py-stats',
    version='0.1',
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),  # Exclude test packages
    entry_points={
        'console_scripts': [
            'git-py-stats=git_py_stats.main:main',
        ],
    },
    install_requires=[
        # Nothing
    ],
    data_files=[
        # Manpages
        ('share/man/man1', ['man/git-py-stats.1']),
    ],
    description='A Python Implementation of git-quick-stats',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Tom Ice',
    license='MIT',
    url='https://github.com/tomice/git-py-stats',
    python_requires='>=3.6',
)

