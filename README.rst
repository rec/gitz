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

`git-fresh <help/git-fresh.rst>`_
  Create and push fresh branches from a reference branch

`git-gitz <help/git-gitz.rst>`_
  Print information about the gitz environment

`git-infer <help/git-infer.rst>`_
  Commit changes with an auto-generated message
  (from https://github.com/moondewio/git-infer)

`git-ls <help/git-ls.rst>`_
  List each file with its most recent commit, in subtle color
  (from an unknown source)

.. image:: img/git-ls-screenshot.png

`git-rotate <help/git-rotate.rst>`_
  Rotate the current branch forward or backward in the list of branches

`git-st <help/git-st.rst>`_
  Colorful, compact git status
  
  This version written by https://github.com/PlatyPew/, original
  version by https://www.reddit.com/user/ex1c)

.. image:: img/git-st-screenshot.png

`git-stripe <help/git-stripe.rst>`_
  Push a sequence of commit IDs to the origin repo

Dangerous commands that delete, rename or overwrite branches
============================================================

`git-copy <help/git-copy.rst>`_
  Copy a git branch locally and on all remotes

`git-delete <help/git-delete.rst>`_
  Delete one or more branches locally and on all remotes

`git-rename <help/git-rename.rst>`_
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

`git-amp <help/git-amp.rst>`_
  AMend just the last commit message and force-Push, somewhat safely

`git-combine <help/git-combine.rst>`_
  Combine multiple commits into one

`git-shuffle <help/git-shuffle.rst>`_
  Reorder and delete commits in the existing branch

`git-snip <help/git-snip.rst>`_
  Edit one or more commits out of history

`git-split <help/git-split.rst>`_
  Split a range of commits into many single-file commits

Dangerous commands that are janky
=================================

``git-all`` is something I use all the time, but it only works in
simple cases, and I don't see a good path to making it do complicated
things in a sane way.

`git-all <help/git-all.rst>`_
  Perform a command on each of multiple branches or directories
