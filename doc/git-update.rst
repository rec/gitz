``git-update``: Update branches from the reference branch
---------------------------------------------------------

USAGE
=====
.. code-block:: bash

    git-update [branch ...branch]

DANGER
======

Rewrites history!

DESCRIPTION
===========

``git-update`` goes to each branch in turn, then tries to update it
the reference branch by pulling with --rebase.

If the rebase fails with a conflict, then ``git-update``aborts the
rebase and returns that branch to its previous condition.

If the rebase succeeds, ``git-update`` force-pushes the result.

EXAMPLES
========

``git-update``
    Updates all branches

``git-update foo bar``
    Only updates branches foo and bar

FLAGS
=====

.. code-block:: bash

    git-update [-h] [-q] [-v] [-f] [-r REFERENCE_BRANCH] [-n] [branches]

Positional arguments:
  ``branches``: A list of branches to update - default is all branches

Optional arguments:
  ``-h, --help``: show this help message and exit

  ``-q, --quiet``: Suppress all output

  ``-v, --verbose``: Report all messages in great detail

  ``-f, --force``: Force push over non-matching remote branches

  ``-r REFERENCE_BRANCH, --reference-branch REFERENCE_BRANCH``: Branch to create from, in the form ``branch`` or ``remote/branch``

  ``-n, --no-run``: If set, commands will be printed but not executed

`Gitz home page <https://github.com/rec/gitz/>`_
================================================
