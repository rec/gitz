``git go``: Open a browser page for the current repo
----------------------------------------------------

USAGE
=====

.. code-block:: bash

    git go [-h] [-q] [-v] [-n] [cmd]

Positional arguments
  ``cmd``: Command to execute - choose from commits directory issues project new_releases
  ``releases``: travis

Optional arguments
  ``-h, --help``: show this help message and exit

  ``-q, --quiet``: Suppress all output

  ``-v, --verbose``: Report all messages in great detail

  ``-n, --no-run``: If set, commands will be printed but not executed

DESCRIPTION
===========

Usage:

  ``git go [<location>]``

where <location> is one or more letters from:

* commits: the list of commits for the current branch (the default)

* directory: the subdirectory in the current branch

* issues: the issues page

* project: the root directory for the project

* new_releases: a form to create new releases

* releases: a list of existing releases

* travis: the Travis page for that repo

EXAMPLES
========

``git go``
