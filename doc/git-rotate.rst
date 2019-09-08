``git rotate``: Rotate the current branch forward or backward in the list of branches
-------------------------------------------------------------------------------------

USAGE
=====

.. code-block:: bash

    git rotate [-h] [-q] [-v] [-n] [steps]

Positional arguments
  ``steps``: Number of steps to rotate (positive or negative)

Optional arguments
  ``-h, --help``: show this help message and exit

  ``-q, --quiet``: Suppress all output

  ``-v, --verbose``: Report all messages in great detail

  ``-n, --no-run``: If set, commands will be printed but not executed

DESCRIPTION
===========

Rotate through the branches in a repo, one at a time, in the order given by
the `git branch` command.

If x is a number, ``git-rotate x`` rotates x branches forward,
and ``git-rotate -x`` rotates x branches forward.

Great for quickly browsing all the branches one at a time.

EXAMPLES
========

``git rotate``
``git rotate 1``
    Rotates to the next branch

``git rotate 3``
    Rotates 3 branches ahead

``git rotate -1``
``git rotate -``
    Rotates 1 branch backward
