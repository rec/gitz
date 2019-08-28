``git-fresh``: Create and push fresh branches from a reference branch
---------------------------------------------------------------------

USAGE
=====
.. code-block:: bash

    git fresh <branch-name> [...<branch-name>]

DESCRIPTION
===========

    Create a branch, fetch the upstream remote, get the commit ID
    of the tip of the reference branch (by default, either develop or master)
    and push to the origin

EXAMPLES
========

    git fresh foo
       Create a new branch foo and push to the origin
    
    git fresh one two three
       Create three new branches

FLAGS
=====

    Full usage: git-fresh [-h] [-q] [-v] [-d] branches [branches ...]
    
    positional arguments:
      branches       Names of branches to create
    
    optional arguments:
      -h, --help     show this help message and exit
      -q, --quiet    Suppress all output
      -v, --verbose  Report all messages in great detail
      -d, --dry-run  If set, commands will be printed but not executed
