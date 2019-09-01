``git-update``: Update a range of commits into many single-file commits
-----------------------------------------------------------------------

USAGE
=====
.. code-block:: bash

    git-update [<pathspec>]

DANGER
======

    Rewrites history!

DESCRIPTION
===========

    `git-update` squashes together a range of commits and the staging area, then
    updates out a sequence of individual commits, one for each file changed.

EXAMPLES
========

    ``git-update``
        Updates the staging area if it's not empty, otherwise HEAD

    ``git-update HEAD``
        Updates the squash of the staging area and HEAD

    ``git-update HEAD~``
        Updates the squash of the staging area, HEAD and HEAD~

FLAGS
=====
    ``git-update [-h] [-q] [-v] [commit]``

    Positional arguments:
      ``commit``: Optional commit ID to update from

    Optional arguments:
      ``-h, --help``: show this help message and exit

      ``-q, --quiet``: Suppress all output

      ``-v, --verbose``: Report all messages in great detail

`Gitz home page <https://github.com/rec/gitz/>`_
================================================
