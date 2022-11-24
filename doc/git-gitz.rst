``git gitz``: Print information about the gitz git commands
-----------------------------------------------------------

USAGE
=====

.. code-block:: bash

    git gitz [-h] [-q] [-v] [-n] [items [items ...]]

Positional arguments
  ``items``: 

Optional arguments
  ``-h, --help``: show this help message and exit

  ``-q, --quiet``: Suppress all output

  ``-v, --verbose``: Report all messages in great detail

  ``-n, --no-run``: If set, commands will be printed but not executed

DESCRIPTION
===========

`git gitz` lists information about the gitz commands.

By default it lists everything, or you can select one or more subcommands:

    commands:
        All the gitz commands

    defaults:
        Default values: protected branches and remotes

    executable_directory:
        The path to the gitz executables,

    home_page:
        The home page of the gitz project

    library_directory:
        The path to the gitz Python library,

    python:
        About the version of Python used

    version:
        The version number of gitz

MOVIE
=====

.. figure:: https://raw.githubusercontent.com/rec/gitz/git-add-improvements/doc/movies/git-gitz.svg?sanitize=true
    :align: center
    :alt: git-gitz.svg

EXAMPLES
========

``git gitz commands``
``git gitz c``
    Prints the list of gitz commands

``git gitz``
``git gitz commands defaults executable_directory home_page library_directory python version``
``git gitz c d e h l p v``
    Prints everything:
        * All the gitz commands
        * Default values: protected branches and remotes
        * The path to the gitz executables,
        * The home page of the gitz project
        * The path to the gitz Python library,
        * About the version of Python used
        * The version number of gitz

``git gitz version exec``
    Print just the version number and the git executable directory
