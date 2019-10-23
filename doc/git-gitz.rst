``git gitz``: Print information about the gitz environment
----------------------------------------------------------

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
        The path to the gitz executable directory,

    home_page:
        The home page of the gitz project

    library_directory:
        The gitz library directory

    version:
        The version number

EXAMPLES
========

``git gitz commands``
``git gitz c``
    Prints the list of gitz commands

``git gitz``
``git gitz commands defaults executable_directory home_page library_directory version``
``git gitz c d e h l v``
    Prints everything:
        * All the gitz commands
        * Default values: protected branches and remotes
        * The path to the gitz executable directory,
        * The home page of the gitz project
        * The gitz library directory
        * The version number

``git gitz version exec``
    Print just the version number and the git executable directory
