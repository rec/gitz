``git-amp``: AMend just the last commit message and force-Push, somewhat safely
-------------------------------------------------------------------------------

USAGE
=====
.. code-block:: bash

    git amp [commit message here]

DANGER
======

    Rewrites history!

DESCRIPTION
===========

    AMend the last commit message and force Push to its upstream branch.
    
    If arguments are given, they are used as the commit message,
    otherwise an editor is brought up to create one.
    
    git-amp rewrites history and should only be used on private branches.
    For your protection, 'git amp' will fail with a message if there are
    any changes in your workspace which would get accidentally mixed into
    the previous commit.

EXAMPLES
========

    ``git amp``
        Bring up an editor for a new commit message, then amend and push

    ``git amp Your new commit message here``
       Amend and push with the message "Your new commit message here"

    ``git amp "Commit message! (fix #12?)"``
        Amend and push with message "Commit message! (fix #12?)"
        (You need quotes if the message includes special shell
         characters like #, ', ", *, ?, !)
