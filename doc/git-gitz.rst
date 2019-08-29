``git-gitz``: Print information about the gitz environment
----------------------------------------------------------

USAGE
=====
.. code-block:: bash

    git gitz [item ..item]

DESCRIPTION
===========

    `git gitz` lists all the gitz commands, the gitz protected branches
    and remotes, or the current gitz version

EXAMPLES
========

    ``git gitz commands defaults directory version``
    ``git gitz``
        Prints all the gitz commands, the variable defaults
        (including protected branches and remotes),
        the version number, and the git command directory

    ``git gitz version directory``
        Print just the version number and the git command directory

FLAGS
=====
    ``git-gitz [-h] [-q] [-v] [-d] [items [items ...]]``

    Positional arguments:
      ``items``: 

    Optional arguments:
      ``-h, --help``: show this help message and exit

      ``-q, --quiet``: Suppress all output

      ``-v, --verbose``: Report all messages in great detail

      ``-d, --dry-run``: If set, commands will be printed but not executed

`Gitz home page <https://github.com/rec/gitz/>`_
================================================