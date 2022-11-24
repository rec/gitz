``git adjust``: Amend any commit, not just the last
---------------------------------------------------

USAGE
=====

.. code-block:: bash

    git adjust [-h] [-q] [-v] [-A] [-a] [-c COMMIT] [-m MESSAGE] [-n] [target]

Positional arguments
  ``target``: Target commit that gets amended

Optional arguments
  ``-h, --help``: show this help message and exit

  ``-q, --quiet``: Suppress all output

  ``-v, --verbose``: Report all messages in great detail

  ``-A, --all-files``: Use all files, even untracked ones

  ``-a, --all-tracked``: Use all staged and tracked files

  ``-c COMMIT, --commit COMMIT``: Commit that is used to amend the target. If empty, use the changes in the staging area.

  ``-m MESSAGE, --message MESSAGE``: If set, use this for the message of the amended commit

  ``-n, --no-run``: If set, commands will be printed but not executed

DESCRIPTION
===========

Amend any commit in the current branch - either with another commit,
or with the contents of the staging area.

DANGER
======

Rewrites history!

MOVIE
=====

.. figure:: https://raw.githubusercontent.com/rec/gitz/git-add-improvements/doc/movies/git-adjust.svg?sanitize=true
    :align: center
    :alt: git-adjust.svg

EXAMPLES
========

``git adjust``
    Amends HEAD with the contents of the staging area.

    Equivalent to ``git commit --amend --no-edit``

``git adjust HEAD~``
    Amends HEAD~ with the contents of the staging area and
    then cherry-picks HEAD back on top of it

``git adjust HEAD~3``
    Amends HEAD~3 with the contents of the staging area, then
    cherry-picks HEAD~2, HEAD~ and HEAD back again on top of it

``git adjust -m "Some message" HEAD~3``
    Amends HEAD~3 with the contents of the staging area and the commit
    message "Some message", then cherry-picks HEAD~2, HEAD~ and HEAD on top

``git adjust HEAD~3 --commit=HEAD~``
    Amends HEAD~3 with HEAD~ and then cherry-picks HEAD~2 and HEAD
    on top of it
