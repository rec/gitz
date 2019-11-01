``git restore``: Save and restore state of the git repository
-------------------------------------------------------------

USAGE
=====

.. code-block:: bash

    git restore [-h] [-q] [-v] [-a] [-n] [state]

Positional arguments
  ``state``: Restore to this state if set. Otherwise, print a commit ID that saves
  ``this``: state.

Optional arguments
  ``-h, --help``: show this help message and exit

  ``-q, --quiet``: Suppress all output

  ``-v, --verbose``: Report all messages in great detail

  ``-a, --all``: Restore even untracked files

  ``-n, --no-run``: If set, commands will be printed but not executed

DESCRIPTION
===========

Saves and restores the exact state of the git repository
including files staged but not commited and unknown files.

DANGER
======

Rewrites history!

EXAMPLES
========

``git restore``
    Prints the commit ID that represents this current state
