``git-split``: Split a range of commits into many single-file commits
---------------------------------------------------------------------

USAGE
=====
.. code-block:: bash

    git-split [<pathspec>]

DANGER
======

    Rewrites history!

DESCRIPTION
===========

    `git-split` squashes together a range of commits and the staging area, then
    splits out a sequence of individual commits, one for each file changed.

EXAMPLES
========

    git-split
        Splits the staging area if it's not empty, otherwise HEAD
    
    git-split HEAD
        Splits the squash of the staging area and HEAD
    
    git-split HEAD~
        Splits the squash of the staging area, HEAD and HEAD~

FLAGS
=====

    Full usage: git-split [-h] [-q] [-v] [commit]
    
    positional arguments:
      commit         Optional commit ID to split from
    
    optional arguments:
      -h, --help     show this help message and exit
      -q, --quiet    Suppress all output
      -v, --verbose  Report all messages in great detail
