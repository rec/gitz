``git rot``: Rotate through branches in a Git repository
--------------------------------------------------------

USAGE
=====

.. code-block:: bash

    git rot [-h] [-q] [-v] [-n] [rotate]

Positional arguments
  ``rotate``: Number of steps to rotate (positive or negative), or a string prefix to match.

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

If N is a string, ``git-rotate <prefix>`` rotates through all branches
starting with that string.

``git-rotate ma`` will rotate through all branches starting with ma


Useful for quickly browsing each branch in a repository one at a time.

MOVIE
=====

.. figure:: https://raw.githubusercontent.com/rec/gitz/git-add-improvements/doc/movies/git-rot.svg?sanitize=true
    :align: center
    :alt: git-rot.svg

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
