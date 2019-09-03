``git-combine``: Combine multiple commits into one
--------------------------------------------------

USAGE
=====
.. code-block:: bash

    git-combine [commit ...commit] [-b/--base=<commit>]

DANGER
======

    Rewrites history!

DESCRIPTION
===========

    Equivalent to hard resetting to the base commit, then cherry picking
    each subsequent commit.
    
    The -s/--squash argument

EXAMPLES
========

    ``git combine d2dfe0c a2833bc``
      Goes to the commit in `master` and then cherry picks the two commits
      d2dfe0c and a2833bc on top of it.

FLAGS
=====
    ``git-combine [-h] [-q] [-v] [-b BASE] [-s SQUASH] [-n] commit_id [commit_id ...]``

    Positional arguments:
      ``commit_id``: List of commit IDs to cherry pick

    Optional arguments:
      ``-h, --help``: show this help message and exit

      ``-q, --quiet``: Suppress all output

      ``-v, --verbose``: Report all messages in great detail

      ``-b BASE, --base BASE``: Base commit to start from

      ``-s SQUASH, --squash SQUASH``: Squash all commits into one, with a message

      ``-n, --no-run``: If set, commands will be printed but not executed

`Gitz home page <https://github.com/rec/gitz/>`_
================================================
