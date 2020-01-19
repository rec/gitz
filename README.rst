🗜 gitz - git commands for rapid development 🗜
------------------------------------------------------

This is a collection of seventeen git utilities aimed at people doing rapid
development using Git.

Gitz is for two types of users - quality-obsessed individuals who relentlessly
manicure their pull requests until every byte is in the right place; and
ultra-rapid developers who want to generate large features quickly while taking
advantage of continuous integration.

Most of these utilities only exist here, one came from a chat on Reddit and
I don't know where one of them came from.

Four of them are written in Bash, the rest use Python 3.  They have been tested
on Mac OS/X (Darwin) and on Ubuntu, and will likely work on any Unix-like
operating system.

How to install
==============

Use `pip <https://pypi.org/project/pip/>`_:

.. code-block:: bash

    pip3 install gitz


Getting help
============

This page contains a summary and a link to a manual page for each command.  From
the terminal, use ``-h`` flag like this: ``git new -h`` or use ``man`` like
this: ``man git-new``.


When to use gitz
=================

1. At the start of a session

   - ``git new`` safely creates fresh branches from upstream

   - ``git update`` for each branch, rebases from upstream and force-pushes

2. During development

   - ``git st`` is a more compact and prettier ``git status``

   - ``git when`` shows you when documents were last changed

3. During rapid development

   - ``git infer`` commits files with an automatically generated message -
     great for committing tiny changes for later rebasing down

4. While cleaning up a branch for review

   - ``git permute`` permutes, squashes or removes commits in the current branch

   - ``git split`` split one or more commits, perhaps with the staging area,
     into many small individual commits, one per file

5. During repository maintenance

   - ``git rotate`` rotates through all branches

   - ``git copy``, ``git delete``,  and ``git rename`` work on both local
     and upstream branches

6. Working with continuous integration

   - ``git stripe`` pushes a sequence of commits to individual remote branches
     where CI can find and test them

The movie
==========

.. figure:: https://asciinema.org/a/McnRqYSxdlfdJdjyG1Rm9x5uU.png
    :target: https://asciinema.org/a/McnRqYSxdlfdJdjyG1Rm9x5uU?autoplay=1&theme=solarized-light&loop=1
    :align: center
    :alt: The whole gitz movie
    :width: 430
    :height: 402

The gitz commands
-----------------


Safe commands
=============

Informational commands that don't change your repository

`git gitz <doc/git-gitz.rst>`_
  Print information about the gitz git commands

`git infer <doc/git-infer.rst>`_
  Commit changes with an automatically generated message

  (from https://github.com/moondewio/git-infer)

`git multi-pick <doc/git-multi-pick.rst>`_
  Cherry-pick multiple commits, with an optional squash

`git new <doc/git-new.rst>`_
  Create and push new branches

`git rotate <doc/git-rotate.rst>`_
  Rotate through branches in a Git repository

`git st <doc/git-st.rst>`_
  Colorful, compact git status

`git stripe <doc/git-stripe.rst>`_
  Push a sequence of commit IDs to a remote repository

`git when <doc/git-when.rst>`_
  For each file, show the most recent commit that changed it.

  Dotfiles are ignored by default.

Dangerous commands that delete, rename or overwrite branches
============================================================

`git copy <doc/git-copy.rst>`_
  Copy a git branch locally and remotely

`git delete <doc/git-delete.rst>`_
  Delete one or more branches locally and remotely

`git rename <doc/git-rename.rst>`_
  Rename a git branch locally and remotely

By default, the branches ``develop`` and ``master`` are protected -
they are not allowed to be copied to, renamed, or deleted.

You can configure this in three ways:

- setting the ``--all/-a`` flag ignore protected branches entirely

- setting the environment variable ``GITZ_PROTECTED_BRANCHES`` overrides these
  defaults

- setting a value for the keys ``PROTECTED_BRANCHES`` in the file
  .gitz.json in the top directory of your Git project has the same effect

Dangerous commands that rewrite history
=======================================

Slice, dice, shuffle and split your commits.

These commands are not intended for use on a shared or production branch, but
can significantly speed up rapid development on private branches.

`git adjust <doc/git-adjust.rst>`_
  Amend any commit, not just the last

`git permute <doc/git-permute.rst>`_
  Reorder and delete commits in the current branch

`git split <doc/git-split.rst>`_
  Split a range of commits into many single-file commits

`git update <doc/git-update.rst>`_
  Update branches from a reference branch
