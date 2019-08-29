``git-shuffle``: Reorder and delete commits in the existing branch
------------------------------------------------------------------

USAGE
=====
.. code-block:: bash

    git-shuffle [permutation]

DANGER
======

    Rewrites history!

DESCRIPTION
===========

    Shuffles the current sequence of commits, perhaps deleting some.

EXAMPLES
========

    ``git shuffle``
    ``git shuffle ba``
    ``git shuffle 10``
    ``git shuffle 21``
        Switches the first and second commit

    ``git shuffle ab``
    ``git shuffle 01``
    ``git shuffle 12``
        Do nothing

    ``git shuffle 312``
    ``git shuffle cab``
    ``git shuffle zxy``
        Cycles the first three commits so the third one is first

    ``git shuffle __321_``
        Deletes the first two commits, reverses the next three, and
        deletes one more.

FLAGS
=====
    ``git-shuffle [-h] [-q] [-v] [-s SQUASH] [-d] shuffle``

    Positional arguments:
      ``shuffle``: Pattern string to shuffle

    Optional arguments:
      ``-h, --help``: show this help message and exit

      ``-q, --quiet``: Suppress all output

      ``-v, --verbose``: Report all messages in great detail

      ``-s SQUASH, --squash SQUASH``: Squash all commits into one, with a message

      ``-d, --dry-run``: If set, commands will be printed but not executed

`Gitz home page <https://github.com/rec/gitz/>`_
================================================
