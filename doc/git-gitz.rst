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

`git gitz` lists information about the gitz commands

EXAMPLES
========

``git gitz``
``git gitz commands defaults exec home_page library version``
``git gitz c d e h l v``
      Prints:
        * all the gitz commands
        * the variable defaults (including protected branches and remotes)
        * the gitz executable directory,
        * the home page of the project
        * the gitz library directory
        * the version number

``git gitz version exec``
    Print just the version number and the git executable directory
