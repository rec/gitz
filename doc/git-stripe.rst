``git stripe``: Push a sequence of commit IDs to a remote repository
--------------------------------------------------------------------

USAGE
=====

.. code-block:: bash

    git stripe [-h] [-q] [-v] [-c COUNT] [-d] [-l] [-o OFFSET] [-r REMOTES] [-s] [-n]
                  [commits [commits ...]]

Positional arguments
  ``commits``: Branch/commit IDs to be striped (defaults to HEAD~)

Optional arguments
  ``-h, --help``: show this help message and exit

  ``-q, --quiet``: Suppress all output

  ``-v, --verbose``: Report all messages in great detail

  ``-c COUNT, --count COUNT``: The number of striped branches to be created

  ``-d, --delete``: Delete all striped branches

  ``-l, --list``: List all remote stripes

  ``-o OFFSET, --offset OFFSET``: Offset to start numbering stripes

  ``-r REMOTES, --remotes REMOTES``: One or more remote remotes to push to, separated by colon. "." means the local repo, "^" means the upstream repo

  ``-s, --safe``: Do not push over existing stripes: find an unused range of indices

  ``-n, --no-run``: If set, commands will be printed but not executed

DESCRIPTION
===========

Starting with a given commit ID, and moving backwards from there,
push each commit ID to its own disposable branch name.

Useful to bring these commits to the attention of your continuous integration
if it has missed some of your commit IDs because you rebased or pushed a
sequences of commits too fast.

MOVIE
=====

.. figure:: https://raw.githubusercontent.com/rec/gitz/master/doc/movies/git-stripe.svg?sanitize=true
    :align: center
    :alt: git-stripe.svg

EXAMPLES
========

``git stripe``
    Pushes HEAD~ into its own branch named _gitz_stripe_0

``git stripe --count=3``
``git stripe -c3``
    Pushes HEAD~, HEAD~2 and HEAD~3 into their own branches named
    _gitz_stripe_0, _gitz_stripe_1 and _gitz_stripe_2

``git stripe --offset=5``
``git stripe -o5``
    Pushes HEAD~, HEAD~2 and HEAD~3 into their own branches named
    _gitz_stripe_5, _gitz_stripe_6 and _gitz_stripe_7

``git stripe 2 HEAD~3``
``git stripe HEAD~3 2``
    Pushes HEAD~3 and HEAD~4 into two branches named _gitz_stripe_0
    and  _gitz_stripe_1

``git stripe --delete-all``
``git stripe -D``
    Delete all stripes
