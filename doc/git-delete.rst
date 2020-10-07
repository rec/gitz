``git delete``: Delete one or more branches locally and remotely
----------------------------------------------------------------

USAGE
=====

.. code-block:: bash

    git delete [-h] [-q] [-v] [--protected] [-n] target [target ...]

Positional arguments
  ``target``: 

Optional arguments
  ``-h, --help``: show this help message and exit

  ``-q, --quiet``: Suppress all output

  ``-v, --verbose``: Report all messages in great detail

  ``--protected``: Delete all, even protected remotes or branches

  ``-n, --no-run``: If set, commands will be printed but not executed

DESCRIPTION
===========

Delete each branch specified together with its remote branch.

By default, branches named `main`, `master` and `develop` are protected,
which means they cannot be deleted.

Using the --all/-a flag allows protected branches to be deleted.

It's also possible to change which branches are protected by setting
the environment variable GITZ_PROTECTED_BRANCHES to a list of
branches separated by colons, or to an empty string to turn off
protection entirely.

DANGER
======

Deletes remote branches!

MOVIE
=====

.. figure:: https://raw.githubusercontent.com/rec/gitz/master/doc/movies/git-delete.svg?sanitize=true
    :align: center
    :alt: git-delete.svg

EXAMPLES
========

``git delete foo bar``
    Delete the branches foo and bar locally and remotely
