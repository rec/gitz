``git-snip``: Edit one or more commits out of history
-----------------------------------------------------

USAGE
=====

.. code-block:: bash

    git-snip [-h] [-q] [-v] [-n] commit_ids [commit_ids ...]

Positional arguments
  ``commit_ids``: Names of commit_ids to create

Optional arguments
  ``-h, --help``: show this help message and exit

  ``-q, --quiet``: Suppress all output

  ``-v, --verbose``: Report all messages in great detail

  ``-n, --no-run``: If set, commands will be printed but not executed

DESCRIPTION
===========

"
Edit one or more commits IDs out of the current branch by index
or by commit ID

IDs 0, 1, 2, 3... are short for HEAD~0, HEAD~1, HEAD~2, HEAD~3...

This command rewrites history and is only intended for use on private
branches.

DANGER
======

Rewrites history!

EXAMPLES
========

``git snip 0``
    Same as git reset --hard HEAD~

``git snip 1 2``
    Remove the two commits HEAD~1 and HEAD~2 but keep HEAD
