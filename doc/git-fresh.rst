``git-fresh``: Create and push one or more fresh branches
---------------------------------------------------------

USAGE
=====
.. code-block:: bash

    git fresh <branch-name> [...<branch-name>]

DESCRIPTION
===========

    Creates one or more fresh branches from the main working branch
    and pushes them them to your git origin.

EXAMPLES
========

    ``git fresh foo``
       Create a new branch foo and push to the origin

    ``git fresh one two three``
       Create three new branches

FLAGS
=====
    ``git-fresh [-h] [-q] [-v] [-d] branches [branches ...]``

    Positional arguments:
      ``branches``: Names of branches to create

    Optional arguments:
      ``-h, --help``: show this help message and exit

      ``-q, --quiet``: Suppress all output

      ``-v, --verbose``: Report all messages in great detail

      ``-d, --dry-run``: If set, commands will be printed but not executed
