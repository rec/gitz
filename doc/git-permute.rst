``git permute``: Reorder and delete commits in the current branch
-----------------------------------------------------------------

USAGE
=====

.. code-block:: bash

    git permute [-h] [-q] [-v] [-s [SQUASH]] [-n] permutation

Positional arguments
  ``permutation``: 
  ``Pattern``: string to permute

Optional arguments
  ``-h, --help``: show this help message and exit

  ``-q, --quiet``: Suppress all output

  ``-v, --verbose``: Report all messages in great detail

  ``-s [SQUASH], --squash [SQUASH]``: Squash all commits into one. If an argument is provided, use it as the commit message.

  ``-n, --no-run``: If set, commands will be printed but not executed

DESCRIPTION
===========

Permutes the commits in the current branch, perhaps deleting some.

For example, ``git permute ba`` switches the first and second most
recent commits, ``git permute cba`` swaps the first and third
commits, ``git permute cab`` pops the third commit to be the most
recent, top commit on the branch.

DANGER
======

Rewrites history!

MOVIE
=====

.. figure:: https://raw.githubusercontent.com/rec/gitz/master/doc/movies/git-permute.svg?sanitize=true
    :align: center
    :alt: git-permute.svg

EXAMPLES
========

``git permute 10``
``git permute ba``
    Switches the first and second most recent commits

``git permute ab``
``git permute abc``
``git permute 01``
``git permute 012``
    Do nothing

``git permute cab``
``git permute 201``
    Cycles the three most recent commits so the third one is first

``git permute edcg``
``git permute 5437``
    Deletes the most recent two commeits, reverses the next three, and
    deletes the sixth.

``git permute edcg -s 'My message'``
``git permute edcg --squash='My message'``
``git permute 5437 -s "My message"``
    Same as the previous command, but squashes the three commits into
    one with the commit message 'My message'
