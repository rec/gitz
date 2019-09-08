``git delete``: Delete one or more branches locally and on all remotes
----------------------------------------------------------------------

USAGE
=====

.. code-block:: bash

    git delete [-h] [-q] [-v] [-f] [-n] target [target ...]

Positional arguments
  ``target``: 

Optional arguments
  ``-h, --help``: show this help message and exit

  ``-q, --quiet``: Suppress all output

  ``-v, --verbose``: Report all messages in great detail

  ``-f, --force``: Delete all, even protected remotes or branches

  ``-n, --no-run``: If set, commands will be printed but not executed

DESCRIPTION
===========

By default, the branches `master` and `develop` and the remote
`upstream` are protected, which means that they are not allowed
to be delete.

Using the --all/-a flag allows protected branches and remotes
to be deleted.

It's also possible to change which branches or remotes are protected
by setting the environment variable GITZ_PROTECTED_BRANCHES or
GITZ_PROTECTED_REMOTES to a list separated by colons, or to an empty
string to turn off protection entirely.

DANGER
======

Deletes remote branches!

EXAMPLES
========

``git delete foo bar``
    Delete the branches foo and bar locally and on every upstream
    except (by default) upstream
