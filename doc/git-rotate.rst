``git rotate``: Rotate through branches in a Git repository
-----------------------------------------------------------

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

Move through the branches in a Git repository in the order
given by the `git branch` command, wrapping around at the end.

If N is a number, ``git-rotate N`` rotates N branches forward,
and ``git-rotate -N`` rotates N branches backward.

``git-rotate`` on its own rotates one branch forward, and
``git-rotate -`` rotates one branch backward.

Useful for quickly browsing each branch in a repository one at a time.

EXAMPLES
========

``git rotate``
``git rotate 1``
``git rotate +``
    Rotates to the next branch

``git rotate 3``
``git rotate +3``
    Rotates 3 branches ahead

``git rotate -1``
``git rotate -``
    Rotates 1 branch backward

``git rotate -2``
    Rotates 2 branches backward
