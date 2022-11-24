``git new``: Create and push new branches
-----------------------------------------

USAGE
=====

.. code-block:: bash

    git new [-h] [-q] [-v] [-c CHERRY_PICK] [-d] [-o ORIGIN] [-s] [-u] [-r REFERENCE_BRANCH] [-n]
               branches [branches ...]

Positional arguments
  ``branches``: Names of branches to create

Optional arguments
  ``-h, --help``: show this help message and exit

  ``-q, --quiet``: Suppress all output

  ``-v, --verbose``: Report all messages in great detail

  ``-c CHERRY_PICK, --cherry-pick CHERRY_PICK``: Name a commit to cherry pick into the new branch

  ``-d, --duplicate``: Duplicate a branch in a remote repo into this repo

  ``-o ORIGIN, --origin ORIGIN``: Remote origin to push to

  ``-s, --stash``: Stash existing changes before creating then unstash

  ``-u, --use-head``: Use HEAD and not reference branch

  ``-r REFERENCE_BRANCH, --reference-branch REFERENCE_BRANCH``: Branch to create from, in the form ``branch`` or ``remote/branch``

  ``-n, --no-run``: If set, commands will be printed but not executed

DESCRIPTION
===========

Create new branches from the reference branch and push them with
--set-upstream.

``git new`` does the things you really want to safely get new branches
where you can start working and pushing immediately

- Fails leaving the workspace unchanged if there are uncommitted changes

- Fails if any of the new branches already exists locally or remotely

- Fetches the *reference branch* only - a branch on the upstream or origin repo
  that is the main branch for development - likely upstream/main or origin/main
  or upstream/master or origin/master

- Create new branches locally from that reference branch commit ID

- Pushes them to the remote origin with --set-upstream

USEFUL FLAGS

``git new --reference/-r <branch-or-commit>`` uses a commit ID
to populate the new branches that isn't the default reference branch

``git new --use-head/-u`` uses the current commit ID to populate the new
branches and not the reference commit

``git new --duplicate/-d <remote>/<branch>`` duplicates the name
and contents of a remote branch in your local repo, super useful for code
reviewing.

gitz can guess what the reference branch and remote origin are, and for
nearly all projects this will be correct, or this can be specified at the
command line, per project, or through environment variables - see ``git gitz``
for more details.

MOVIE
=====

.. figure:: https://raw.githubusercontent.com/rec/gitz/git-add-improvements/doc/movies/git-new.svg?sanitize=true
    :align: center
    :alt: git-new.svg

EXAMPLES
========

``git new foo``
    Create a new branch foo from the reference branch and push to the origin

``git new foo --origin=remote_1``
``git new foo -o remote_1``
    Create a new branch foo from the reference branch and push to remote_1

``git new one two three --reference-branch=some-remote/main``
``git new one two three -r some-remote/main``
    Create three new branches from the remote branch some-remote/main
