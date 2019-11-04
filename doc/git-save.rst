``git save``: Save and restore state of the git repository
----------------------------------------------------------

USAGE
=====

.. code-block:: bash

    git save [-h] [-q] [-v] [-a] [-d] [-n] [state]

Positional arguments
  ``state``: Save to this state if set. Otherwise, print a commit ID that saves this
  ``state.``: 

Optional arguments
  ``-h, --help``: show this help message and exit

  ``-q, --quiet``: Suppress all output

  ``-v, --verbose``: Report all messages in great detail

  ``-a, --all``: Save even untracked files

  ``-d, --do_not_stash``: If set, do not stash the commit ID, just print it out

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

``git save``
    Prints the commit ID that represents this current state
