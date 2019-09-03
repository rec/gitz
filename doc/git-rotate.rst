``git-rotate``: Rotate the current branch forward or backward in the list of branches
-------------------------------------------------------------------------------------

USAGE
=====
.. code-block:: bash

    git rotate [<number-of-positions>]

DESCRIPTION
===========

Change the current branch by rotating through all the branches for
this repo in the order given by the `git branch` command

EXAMPLES
========

``git rotate``
    Rotate to the next branch

``git rotate 3``
    Rotate 3 branches ahead

``git rotate -1``
``git rotate -``
    Rotate 1 branch backward

FLAGS
=====

.. code-block:: bash

    git-rotate [-h] [-q] [-v] [-n] [steps]

Positional arguments:
  ``steps``: Number of steps to rotate (positive or negative)

Optional arguments:
  ``-h, --help``: show this help message and exit

  ``-q, --quiet``: Suppress all output

  ``-v, --verbose``: Report all messages in great detail

  ``-n, --no-run``: If set, commands will be printed but not executed

`Gitz home page <https://github.com/rec/gitz/>`_
================================================
