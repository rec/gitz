🗜 gitz - tiny useful git commands, some dangerous 🗜
------------------------------------------------------

This is a collection of a dszen git utilities, each of which does one
useful thing well.

Most of them only exist here, one comes from other git repos, one came from a
chat on Reddit and I don't know where one of them came from

Nine of them are written in Python 3, the rest use Bash.

There's a summary of what each command does below - for more details use the
``-h`` flag like this:

.. code-block:: bash

    git all -h

How to install
==============

If you have ``pip`` installed

.. code-block:: bash

    pip3 install gitz

Otherwise, download and uncompress
`this directory
<https://github.com/rec/gitz/archive/master.tar.gz>`_,
then put that directory's path into the ``PATH`` environment variable.

Getting help
============

Each command has detailed help available by calling it with the -f flag, like
this: ``git all -h``.

A summary of the commands follows:


Safe commands
=============

Informational commands that don't change your repository

``git-fresh``
  Create and push fresh branches from a reference branch

``git-gitz``
  Print information about the gitz environment

``git-infer``
  Commit changes with an auto-generated message
  (from https://github.com/moondewio/git-infer)

``git-ls``
  List each file with its most recent commit, in subtle color

.. image:: img/git-ls-screenshot.png
  (from an unknown source)

.. image:: img/git-ls-screenshot.png

``git-rotate``
  Rotate the current branch forward or backward in the list of branches

``git-st``
  Colorful, compact git status

.. image:: img/git-st-screenshot.png
  

.. image:: img/git-st-screenshot.png
  This version written by https://github.com/PlatyPew/, original

.. image:: img/git-st-screenshot.png
  version by https://www.reddit.com/user/ex1c)

.. image:: img/git-st-screenshot.png

``git-stripe``
  Push a sequence of commit IDs onto upstream branches

Dangerous commands that delete, rename or overwrite branches
============================================================

``git-copy``
  Copy a git branch locally and on all remotes

``git-delete``
  Delete one or more branches locally and on all remotes

``git-rename``
  Rename a git branch locally and on all remotes

By default, the branches ``develop`` and ``master`` and the remote ``upstream``
are not allowed to be copied, renamed, or deleted.

You can disable this by setting the ``--all/-a`` flag, or you can override the
protected branches or remotes by setting the environment variables
``PROTECTED_BRANCHES`` or ``PROTECTED_REMOTES``

Dangerous commands that rewrite history
=======================================

These commands are not intended for use on a shared or production branch, but
can significantly speed up rapid development on private branches.

``git-amp``
  AMend just the last commit message and force-Push, somewhat safely

``git-combine``
  Combine multiple commits into one

``git-shuffle``
  Reorder and delete commits in the existing branch

``git-snip``
  Edit one or more commits out of history

``git-split``
  Split a range of commits into many single-file commits

Dangerous commands that are janky
=================================

``git-all`` is something I use all the time, but it only works in
simple cases, and I don't see a good path to making it do complicated
things in a sane way.

``git-all``
  Perform a command on each of multiple branches or directories
