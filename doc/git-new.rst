``git-new``: Create and push new branches
-----------------------------------------

USAGE
=====

.. code-block:: bash

    git-new [-h] [-q] [-v] [-f] [-o ORIGIN] [-r REFERENCE_BRANCH] [-n] branches [branches ...]

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

Create new branches from the reference branch and push them with
--set-upstream.

git-new does the things you really want to safely get new branches
where you can start working and pushing immediately

- Fails leaving the workspace unchanged if there are uncommitted changes

- Fails if any branch already exists locally or remotely, unless -f/--force

- Fetches the *reference branch* - a branch on the upstream or origin repo that
  is the main branch for development - likely upstream/master or origin/master

- Create new branches locally from that reference branch commit ID

- Pushes them to the remote origin with --set-upstream

gitz can guess what the reference branch and remote origin are, and for
nearly all projects this will be correct, or this can be specified at the
command line, per project, or through environment variables - see ``git gitz``
for more details.

EXAMPLES
========

``git new foo``
   Create a new branch foo from the reference branch and push to the origin

``git new foo --origin=remote_1``
``git new foo -o remote_1``
   Create a new branch foo from the reference branch and push to remote_1

``git new one two three --reference-branch=some-remote/master``
``git new one two three -r some-remote/master``
   Create three new branches from the remote branch some-remote/master
