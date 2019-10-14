``git stripe``: Push a sequence of commit IDs to a remote repository
--------------------------------------------------------------------

USAGE
=====

.. code-block:: bash

    git stripe [-h] [-q] [-v] [-D] [-d] [-f] [-o OFFSET] [-p PREFIX] [-r REMOTES]
                  [-n]
                  [count] [commit_id]

Positional arguments
  ``count``: The number of stripe branches to be created
  ``commit_id``: Branch/commit ID of the first stripe (or HEAD~ if none)

Optional arguments
  ``-h, --help``: show this help message and exit

  ``-q, --quiet``: Suppress all output

  ``-v, --verbose``: Report all messages in great detail

  ``-D, --delete-all``: Delete all striped branches

  ``-d, --delete``: Delete the striped branches for this request

  ``-f, --force``: Force push over existing stripes

  ``-o OFFSET, --offset OFFSET``: Offset to start numbering stripes

  ``-p PREFIX, --prefix PREFIX``: Base name for stripe branches (_gitz_stripe_ if none)

  ``-r REMOTES, --remotes REMOTES``: One or more remote remotes to push to, separated by colon. "." means the local repo, "^" means the upstream repo

  ``-n, --no-run``: If set, commands will be printed but not executed

DESCRIPTION
===========

Starting with a given commit ID, and moving backwards from there,
push each commit ID to its own disposable branch name.

Useful to bring these commits to the attention of your continuous integration
if it has missed some of your commit IDs because you rebased or pushed a
sequences of commits too fast.

EXAMPLES
========

``git stripe``
    Pushes HEAD~, HEAD~2 and HEAD~3 into their own branches named
    _gitz_stripe_0, _gitz_stripe_1 and _gitz_stripe_2

``git stripe 1``
    Pushes HEAD~ into its own branch named _gitz_stripe_0

``git stripe --offset=5``
``git stripe -o5``
    Pushes HEAD~, HEAD~2 and HEAD~3 into their own branches named
    _gitz_stripe_5, _gitz_stripe_6 and _gitz_stripe_7

``git stripe 2 HEAD~3``
``git stripe HEAD~3 2``
    Pushes HEAD~3 and HEAD~4 into two branches named _gitz_stripe_0
    and  _gitz_stripe_1

``git stripe --delete``
``git stripe -d``
    Delete any branches named _gitz_stripe_0, _gitz_stripe_1
    aor _gitz_stripe_2

    git stripe -d does not fail if some or all of the branches
    to be deleted are missing

``git stripe --prefix=MINE``
``git stripe -p MINE``
    Pushes HEAD~, HEAD~2 and HEAD~3 into their own branches named
    MINE_0, MINE_1, MINE_2

``git stripe 2 --prefix=MINE``
``git stripe 2 -p=MINE``
    Pushes HEAD~ and HEAD~2 into their own branches named MINE_0
    and MINE_1

``git stripe 2 --prefix=MINE --offset``
``git stripe 2 -p MINE -o10``
    Pushes HEAD~ and HEAD~2 into their own branches named MINE_10
    and MINE_11
