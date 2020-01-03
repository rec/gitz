``git shuffle``: Reorder and delete commits in the current branch
-----------------------------------------------------------------

USAGE
=====

.. code-block:: bash

    git shuffle [-h] [-q] [-v] [-s [SQUASH]] [-n] shuffle

Positional arguments
  ``shuffle``: Pattern string to shuffle (defaults to "ba")

Optional arguments
  ``-h, --help``: show this help message and exit

  ``-q, --quiet``: Suppress all output

  ``-v, --verbose``: Report all messages in great detail

  ``-s [SQUASH], --squash [SQUASH]``: Squash all commits into one. If an argument is provided, use it as the commit message.

  ``-n, --no-run``: If set, commands will be printed but not executed

DESCRIPTION
===========

Shuffles the commits in the current branch, perhaps deleting some.

For example, ``git shuffle ba`` switches the first and second most
recent commits, ``git shuffle cba`` swaps the first and third
commits, ``git shuffle cab`` pops the third commit to be the most
recent, top commit on the branch.

DANGER
======

Rewrites history!

MOVIE
=====

.. figure:: https://raw.githubusercontent.com/rec/gitz/master/doc/movies/git-shuffle.svg?sanitize=true
    :align: center
    :alt: git-shuffle.svg

EXAMPLES
========

``git shuffle 10``
``git shuffle ba``
    Switches the first and second most recent commits

``git shuffle ab``
``git shuffle abc``
``git shuffle 01``
``git shuffle 012``
    Do nothing

``git shuffle cab``
``git shuffle 201``
    Cycles the three most recent commits so the third one is first

``git shuffle edcg``
``git shuffle 5437``
    Deletes the most recent two commeits, reverses the next three, and
    deletes the sixth.

``git shuffle edcg -s 'My message'``
``git shuffle edcg --squash='My message'``
``git shuffle 5437 -s "My message"``
    Same as the previous command, but squashes the three commits into
    one with the commit message 'My message'
