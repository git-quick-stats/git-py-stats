from setuptools import setup, find_packages

setup(
    name='git-py-stats',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'git-py-stats=git_py_stats.main:main',
        ],
    },
    install_requires=[
        # Nothing
    ],
    description='A Python Implementation of git-quick-stats',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Tom Ice',
    license='MIT',
    url='https://github.com/tomice/git-py-stats',
)

