🗜 gitz - tiny useful git commands, some dangerous 🗜
-------------------------------------------------------------------

This is a collection of eight little git utilities, each of which does one
useful thing well.

Three of them come from scattered open source repositories which I grabbed,
and the other five only exist here.

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

``git-listall``
  List recent commits for multiple branches (Python)

``git-open``
  Opens the GitHub page for a repo/branch in your browser
  (from https://github.com/paulirish/git-open)

``git-st``
  Pretty, compact alternative to ``git-status`` (from
  https://www.reddit.com/user/ex1c)

Dangerous commands
====================

These commands rewrite history extensively and are intended for rapid
development on at on private branches only.

``git-amp``
  AMend the last commit message and force-Push, somewhat safely

``git-rename``
  Renames a git branch _and_ its remote branch

``git-snip``
  Delete one or more commits by commit id or position (Python)

``git-split``
  Split a commit into individual changes, one per file (Python)
