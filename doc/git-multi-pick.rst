``git multi-pick``: Cherry-pick multiple commits, with an optional squash
-------------------------------------------------------------------------

USAGE
=====

.. code-block:: bash

    git multi-pick [-h] [-q] [-v] [-s [SQUASH]] [-n] commit_ids [commit_ids ...]

Positional arguments
  ``commit_ids``: List of commit IDs to cherry pick

Optional arguments
  ``-h, --help``: show this help message and exit

  ``-q, --quiet``: Suppress all output

  ``-v, --verbose``: Report all messages in great detail

  ``-s [SQUASH], --squash [SQUASH]``: Squash all commits into one. If an argument is provided, use it as the commit message.

  ``-n, --no-run``: If set, commands will be printed but not executed

DESCRIPTION
===========

Cherry pick each commit one after another.

If there is a -s/--squash argument, squash the commits down into one,
using the argument to -s/--squash as the commit message.

MOVIE
=====

.. figure:: https://raw.githubusercontent.com/rec/gitz/git-add-improvements/doc/movies/git-multi-pick.svg?sanitize=true
    :align: center
    :alt: git-multi-pick.svg

EXAMPLES
========

``git multi-pick d2dfe0c a2833bc``
  Cherry-picks the commit d2dfe0c and then a2833bc on top of it.

``git multi-pick d2dfe0c a2833bc --squash='Squashed commit!'``
  Cherry-picks the commit d2dfe0c and then a2833bc on top of it,
  and then squashes them into one commit with the commit message
  'Squashed commit!'
