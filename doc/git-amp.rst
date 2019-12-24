``git amp``: AMend the last commit message and force-Push, somewhat safely
--------------------------------------------------------------------------

USAGE
=====

.. code-block:: bash

    git amp [commit message here]

DESCRIPTION
===========

AMend the last commit message and force-Push to its upstream branch.

If arguments are given, they are used as the commit message,
otherwise an editor is brought up to create edit the previous message.

If that is successful, uses git push --force-with-lease to
rewrite the previous commit immediately.

git amp rewrites history and should only be used on private branches.

For your protection, 'git amp' will fail with a message if there are
any changes in your workspace which would get accidentally mixed into
the previous commit.

DANGER
======

Rewrites history!

MOVIE
=====

.. figure:: https://raw.githubusercontent.com/rec/gitz/master/doc/movies/git-amp.svg?sanitize=true
    :align: center
    :alt: git-amp.svg

EXAMPLES
========

``git amp``
    Bring up an editor for a new commit message, then amend and push

``git amp Some commit message here``
    Amend and push with the new message "Some commit message here"

``git amp "Commit message! (fix #127)"``
    Amend and push with message "Commit message! (fix #127)"
    (You need quotes if the message includes special shell
    characters like (, ), #, !, etc.)
