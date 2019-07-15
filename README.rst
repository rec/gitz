🗜 gitz - tiny useful git commands, some dangerous 🗜XX
-------------------------------------------------------------------

This is a collection of a dozen little git utilities, each of which does one
useful thing well.

* Eight only exist here
* Two come from other git repos
* One came from a chat on Reddit
* I don't know where one of them came from

Three of them use Python 3, the rest use Bash.

There's a summary of what each command does below - for more details use the
``-h`` flag like this:

.. code-block:: bash

    git add -h
    git

How to install
================

If you have ``pip`` installed

.. code-block:: bash

    pip3 install gitz

Otherwise, download and unzip
`this directory
<https://github.com/rec/gitz/archive/master.zip>`_,
then put that directory's path into the ``PATH`` environment variable.

Getting help
==============

Each command has detailed help available by calling it with the -f flag,
like this: ``git all -h``.

A summary of all the commands is below.


Safe commands (that don't rewrite history)
=============================================

``git-all``
  Perform a command on each of multiple branches or directories.

``git-rot``
  Rotate the current branch forward or backward in the list of branches

``git-ls``
  Like ``ls`` but shows git info, with good use of color
  (from an unknown source)

``git-infer``
  Commit changes with an auto-generated message
  (from https://github.com/moondewio/git-infer)

``git-open``
  Opens the GitHub page for a repo/branch in your browser
  (from https://github.com/paulirish/git-open)

``git-st``
  Pretty, compact alternative to ``git-status``
  (from https://www.reddit.com/user/ex1c)

Slightly dangerous commands (that move branches around)
=======================================================

``git-copy``
  Copy a branch locally and on every remote

``git-rename``
  Rename a branch locally and on every remote

By default, the branches ``develop`` and ``master`` and the remote ``upstream``
are not allowed to be copied or renamed to.  You can override these by setting
the environment variables ``PROTECTED_BRANCHES`` or ``PROTECTED_REMOTES`` - see
the


More dangerous commands (that rewrite history)
==============================================

These commands are not intended for use on a shared or production branch,
but can significantly speed up rapid development on private branches.

``git-amp``
  AMend just the last commit message and force-Push, somewhat safely

``git-combine``
  Combine multiple commits into one

``git-snip``
  Edit one or more commits out of history

``git-split``
  Split a commit into individual changes, one per file
