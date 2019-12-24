``git copy``: Copy a git branch locally and remotely
----------------------------------------------------

USAGE
=====

.. code-block:: bash

    git copy [-h] [-q] [-v] [-p] [-f] [-n] source [target]

Positional arguments
  ``source``: 
  ``target``: 

Optional arguments
  ``-h, --help``: show this help message and exit

  ``-q, --quiet``: Suppress all output

  ``-v, --verbose``: Report all messages in great detail

  ``-p, --protected``: Copy all, even protected remotes or branches

  ``-f, --force``: Force copy over existing branches

  ``-n, --no-run``: If set, commands will be printed but not executed

DESCRIPTION
===========

Copy one branch to another, both locally and in remote
branches.  If no source branch is given, the current branch is
used.

By default, the branches `master` and `develop`, which means that they are not
allowed to be copied over to.

Using the --all/-a flag allows protected branches to be copied.

It's also possible to override the protected branches by setting the
environment variable GITZ_PROTECTED_BRANCHES to a list separated by colons,
or an empty string for no protection.

DANGER
======

Changes remote branches!

MOVIE
=====

.. figure:: https://raw.githubusercontent.com/rec/gitz/master/doc/movies/git-copy.svg?sanitize=true
    :align: center
    :alt: git-copy.svg

EXAMPLES
========

``git copy old new``
    Copy the branch "old" to "new", both locally and the remote
    repository.

    Fails if "new" exists locally or in the remote repositories.

``git copy -a old new``
``git copy --all old new``
    Copy the branch "old" to "new", both locally and on the
    remote repository, even protected branches or repositories.

    Fails if "new" exists locally or in the remote repositories.

``git copy -f old new``
``git copy --force old new``
    Copy the branch "old" to "new", both locally and on the upstream
    remote repository.

    Overwrites "new" if it exists locally or in the remote repository.
