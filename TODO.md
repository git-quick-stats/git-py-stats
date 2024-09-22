# TODO

* Create a full unit test suite
  - Only some generic tests are currently done
* Create pipelines for when you commit
  - Test suite should run when someone submits a PR in GitHub
* Add configuration similar to how `git-quick-stats` does it
  - Maybe play around with a config file as an option that the user can save
* Add screenshots to README.md
* Structure could probably use a slight adjustment
  - Right now, it's fairly small so we can deal with all of the source files
    being co-located. As it grows, it might be better to create a logical
    folder structure for everything. Be mindful of how imports will work
* Review imports
  - I hate dealing with imports. There's always the battle between absolute
    and implicit with many people have their own opinions on how it should be
    handled. This will go hand-in-hand with the folder structure task
* Handle file generation better
  - Right now, we just blast a file on the filesystem. Should we warn the user
    if one exists already? Should we generate another and subtly rename it?
* Triple-check all functions perform exactly as they do in `git-quick-stats`
  - Some of the file generation isn't quite 1:1.
* Run a pep8 linter on this
  - flake8 should work.
    `flake8 git_py_stats --max-line-length=120 --statistics --count`
    or something
