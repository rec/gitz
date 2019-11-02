``git adjust``: Amend any commit
--------------------------------

USAGE
=====

.. code-block:: bash

    git adjust [-h] [-q] [-v] [-m MESSAGE] [-n] [target] [edit]

Positional arguments
  ``target``: Target commit that gets amended
  ``edit``: Edit commit that is used to amend the target.If empty, use the changes in the staging area.

Optional arguments
  ``-h, --help``: show this help message and exit

  ``-q, --quiet``: Suppress all output

  ``-v, --verbose``: Report all messages in great detail

  ``-m MESSAGE, --message MESSAGE``: If set, use this for the message of the amended commit

  ``-n, --no-run``: If set, commands will be printed but not executed

DESCRIPTION
===========

Amend any commit in the current branch - either with another commit,
or with the contents of the staging area.

DANGER
======

Rewrites history!

EXAMPLES
========

``git adjust``
    Amends HEAD with the contents of the staging area.

    Equivalent to ``git commit --amend --no-edit``

``git adjust HEAD~``
    Amends HEAD~ with the contents of the staging area and
    then cherry-picks HEAD on top of it

``git adjust HEAD~3``
    Amends HEAD~3 with the contents of the staging area and then
    cherry-picks HEAD~2, HEAD~ and HEAD on top of it

``git adjust HEAD~3 HEAD~``
    Amends HEAD~3 with HEAD~ and then cherry-picks HEAD~2 and HEAD
    on top of it
