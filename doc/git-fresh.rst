``git-fresh``: Create and push one or more fresh branches
---------------------------------------------------------

USAGE
=====

.. code-block:: bash

    git-fresh [-h] [-q] [-v] [-f] [-o ORIGIN] [-r REFERENCE_BRANCH] [-n] branches [branches ...]

Positional arguments
  ``branches``: Names of branches to create

Optional arguments
  ``-h, --help``: show this help message and exit

  ``-q, --quiet``: Suppress all output

  ``-v, --verbose``: Report all messages in great detail

  ``-f, --force``: Force push over existing branches

  ``-o ORIGIN, --origin ORIGIN``: Remote origin to push to

  ``-r REFERENCE_BRANCH, --reference-branch REFERENCE_BRANCH``: Branch to create from, in the form ``branch`` or ``remote/branch``

  ``-n, --no-run``: If set, commands will be printed but not executed

DESCRIPTION
===========

Creates one or more fresh branches from the base working branch
and pushes them them to your git origin.

EXAMPLES
========

``git fresh foo``
   Create a new branch foo and push to the origin

``git fresh one two three``
   Create three new branches
