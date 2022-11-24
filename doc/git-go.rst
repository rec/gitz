``git go``: Open a browser page for the current repo
----------------------------------------------------

USAGE
=====

.. code-block:: bash

    git go [-h] [-q] [-v] [--count COUNT] [-n] [cmd] [files [files ...]]

Positional arguments
  ``cmd``: Command to execute - choose from between commits directory files history issues
  ``new_releases``: pulls releases source travis
  ``files``: Zero or more files (for `git open file` or `history`)

Optional arguments
  ``-h, --help``: show this help message and exit

  ``-q, --quiet``: Suppress all output

  ``-v, --verbose``: Report all messages in great detail

  ``--count COUNT, -c COUNT``: Count of versions to display, 0 means all (for `git open history`)

  ``-n, --no-run``: If set, commands will be printed but not executed

DESCRIPTION
===========

Usage:

  ``git go [<location>]``

where <location> is one or more letters from:

* between: open *all* commits between HEAD and main or master

* commits: the list of commits for the current branch (the default)

* directory: the subdirectory in the current branch

* files : open the source for specific files

* history: open *multiple* historical versions of a file

* issues: the issues page

* new_releases: a form to create new releases

* pull: open the form for a pull request

* releases: a list of existing releases

* source: the root directory for the branch

* travis: the Travis page for that repo

EXAMPLES
========

``git go``
