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

The single argument is a pattern where underscores mean commits to be
deleted, and alphabetic characters mean commits to be shuffled.

For example, ``git shuffle ba`` switches the first and second most
recent commits, ``git shuffle cba`` swaps the first and third
commits, ``git shuffle cab`` pops the third commit to be the most
recent, top commit on the branch.

``git shuffle _ba`` deletes the most recent commit and then swaps
the next two; and ``git shuffle _a_b_c`` deletes the most recent, the
third most recent and the fifth most recent commit from the branch.

If omitted, the default pattern is ``ba``.  Only the order of the
letters matter so ``cba``, ``ZYX`` and ``zma`` mean the same thing.

DANGER
======

Rewrites history!

EXAMPLES
========

``git shuffle``
``git shuffle ba``
``git shuffle YX``
``git shuffle 10``
``git shuffle 21``
    Switches the first and second most recent commits

``git shuffle ab``
``git shuffle abc``
``git shuffle ADE``
``git shuffle 01``
``git shuffle 12``
    Do nothing

``git shuffle 312``
``git shuffle cab``
``git shuffle zxy``
    Cycles the three most recent commits so the third one is first

``git shuffle __cba_``
    Deletes the most recent two commeits, reverses the next three, and
    deletes the sixth.

``git shuffle __cba_ -s "My message"``
``git shuffle __cba_ --squash="My message"``
    Same as the previous command, but squashes the three commits into
    one with the commit message "My message"
