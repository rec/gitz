``git split``: Split a range of commits into many single-file commits
---------------------------------------------------------------------

USAGE
=====

.. code-block:: bash

    git split [-h] [-q] [-v] [-p PREFIX] [commit]

Positional arguments
  ``commit``: Optional commit ID to split from

Optional arguments
  ``-h, --help``: show this help message and exit

  ``-q, --quiet``: Suppress all output

  ``-v, --verbose``: Report all messages in great detail

  ``-p PREFIX, --prefix PREFIX``: Prefix for each commit message

DESCRIPTION
===========

`git split` squashes together a range of commits and the staging area, then
splits out a sequence of individual commits, one for each file changed.

DANGER
======

Rewrites history!

MOVIE
=====

.. figure:: https://raw.githubusercontent.com/rec/gitz/master/doc/movies/git-split.svg?sanitize=true
    :align: center
    :alt: git-split.svg

EXAMPLES
========

``git split``
    Split the staging area if it's not empty, otherwise HEAD

``git split HEAD``
    Split the squash of the staging area and HEAD

``git split HEAD~``
    Split the squash of the staging area, HEAD and HEAD~
