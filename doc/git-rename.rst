``git rename``: Rename a git branch locally and remotely
--------------------------------------------------------

USAGE
=====

.. code-block:: bash

    git rename [-h] [-q] [-v] [-p] [-f] [-n] source [target]

Positional arguments
  ``source``: 
  ``target``: 

Optional arguments
  ``-h, --help``: show this help message and exit

  ``-q, --quiet``: Suppress all output

  ``-v, --verbose``: Report all messages in great detail

  ``-p, --protected``: Rename all, even protected remotes or branches

  ``-f, --force``: Force rename over existing branches

  ``-n, --no-run``: If set, commands will be printed but not executed

DESCRIPTION
===========

Rename one branch to another, both locally and in remote
branches.  If no source branch is given, the current branch is
used.

By default, the branches `master` and `develop`, which means that they are not
allowed to be renamed from or two to.

Using the --all/-a flag allows protected branches to be renamed.

It's also possible to override the protected branches by setting the
environment variable GITZ_PROTECTED_BRANCHES to a list separated by colons,
or an empty string for no protection.

DANGER
======

Changes remote branches!

MOVIE
=====

.. figure:: https://raw.githubusercontent.com/rec/gitz/master/doc/movies/git-rename.svg?sanitize=true
    :align: center
    :alt: git-rename.svg

EXAMPLES
========

``git rename old new``
    Rename the branch "old" to "new", both locally and the remote
    repository.

    Fails if "new" exists locally or in the remote repositories.

``git rename -a old new``
``git rename --all old new``
    Rename the branch "old" to "new", both locally and on the
    remote repository, even protected branches or repositories.

    Fails if "new" exists locally or in the remote repositories.

``git rename -f old new``
``git rename --force old new``
    Rename the branch "old" to "new", both locally and on the upstream
    remote repository.

    Overwrites "new" if it exists locally or in the remote repository.
