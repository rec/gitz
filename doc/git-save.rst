``git save``: Save and restore state of the git repository
----------------------------------------------------------

USAGE
=====

.. code-block:: bash

    git save [-h] [-q] [-v] [-a] [-d] [-n] [state]

Positional arguments
  ``state``: Save to this state if set. Otherwise, print a commit ID that saves this state.

Optional arguments
  ``-h, --help``: show this help message and exit

  ``-q, --quiet``: Suppress all output

  ``-v, --verbose``: Report all messages in great detail

  ``-a, --all``: Save even untracked files

  ``-d, --do_not_stash``: If set, do not stash the commit ID, just print it out

  ``-n, --no-run``: If set, commands will be printed but not executed

DESCRIPTION
===========

Saves and restores the whole state of the git repository
including files staged but not commited, and (optionally) untracked
files.

---

You don't need to understand the following to use git-save.
This is just for people who need to know how things work behind the
scenes.

A git-save "record" has up to five parts:

1. The most recent commit (HEAD at the time that git-save was called)
2. Modified, staged files
3. Modified, unstaged files
4. Untracked files
5. The hash stash

git-save starts at HEAD, and adds "hidden" commits for any of
parts 2, 3 and 4 which is non-empty, to get a "final" commit ID.

Finally, the hash stash!  A tiny text file is added after these which
contains only the hash of the final commit, and then this is stashed.

When restoring a save file, the hash is popped from the stash to
``git reset`` to the "final" commit ID, and then working backwards to HEAD
restores the full state.

DANGER
======

Rewrites history!

EXAMPLES
========

``git save``
    Saves everything except untracked files

``git save -a``
``git save --all``
    Saves everything including untracked files: only .gitignored files
    will not be saved this way.
