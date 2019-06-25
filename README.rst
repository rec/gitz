🗜 gitz - tiny useful git commands, some dangerous 🗜
-------------------------------------------------------------------

This is a collection of a dozen little git utilities, each of which does one
useful thing well.

* Eight only exist here
* Two come from other git repos
* One came from a chat on Reddit
* I don't know where one of them came from

Three of them use Python 3, the rest use Bash.

There's a summary of what each command does below - for more details use

.. code-block:: bash

    git <command> -h

Safe commands
===============

Commands that don't rewrite history.

``git-infer``
  Commit changes with an auto-generated message
  (from https://github.com/moondewio/git-infer)

``git-ls``
  Like ``ls`` but shows git info, with good use of color
  (from ??)

``git-loga``
  List recent commits for multiple branches

``git-logr``
  List recent commits for multiple repositories

``git-open``
  Opens the GitHub page for a repo/branch in your browser
  (from https://github.com/paulirish/git-open)

``git-rot``
  Changes the current branch by rotating forward or backward in the branch list

``git-st``
  Pretty, compact alternative to ``git-status``
  (from https://www.reddit.com/user/ex1c)

Dangerous commands
====================

These commands rewrite history and are intended for rapid development on private
branches.

``git-amp``
  AMend the last commit message and force-Push, somewhat safely

``git-combine``
  Combines multiple commit IDs together using cherry picking

``git-rename``
  Renames a git branch _and_ its remote branch

``git-snip``
  Delete one or more commits by commit id or position

``git-split``
  Split a commit into individual changes, one per file
