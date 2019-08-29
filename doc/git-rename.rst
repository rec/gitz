``git-rename``: Rename a git branch locally and on all remotes
--------------------------------------------------------------

USAGE
=====
.. code-block:: bash

    git rename [<source-branch>] <target-branch>

DANGER
======

    Changes remote branches!

DESCRIPTION
===========

    Rename one branch to another, both locally and in remote
    branches.  If no source branch is given, the current branch is
    used.
    
    By default, the branches `master` and `develop` and the remote
    `upstream` are protected, which means that they are not allowed
    to be renamed from or to.
    
    Using the --all/-a flag allows protected branches and remotes
    to be renamed.
    
    It's also possible to override the protected branches or the
    protected remotes by setting one of the environment variables
    GITZ_PROTECTED_BRANCHES or GITZ_PROTECTED_REMOTES
    to a list separated by colons, or an empty string for no protection.

EXAMPLES
========

    ``git rename old new``
        Rename the branch "old" to "new", both locally and in remote
        repositories where the branch "old" exists.

        Fails if "new" exists locally or in the remote repositories.

    ``git rename -c old new``
    ``git rename --create old new``
        Rename the branch "old" to "new", both locally and in remote
        repositories, even ones where the branch "old" does not exist

        Fails if "new" exists locally or in the remote repositories.

    ``git rename -a old new``
    ``git rename --all old new``
        Rename the branch "old" to "new", both locally and in remote
        repositories, even protected branches or repositories.

        Fails if "new" exists locally or in the remote repositories.

    ``git rename -f old new``
    ``git rename --force old new``
        Rename the branch "old" to "new", both locally and in remote
        repositories where the branch "old" exists.

        Overwrites "new" if it exists locally or in the remote repositories.

FLAGS
=====
    ``git-rename [-h] [-q] [-v] [-a] [-c] [-f] [-d] source [target]``

    Positional arguments:
      ``source``: 
      ``target``: 

    Optional arguments:
      ``-h, --help``: show this help message and exit

      ``-q, --quiet``: Suppress all output

      ``-v, --verbose``: Report all messages in great detail

      ``-a, --all``: Rename all, even protected remotes or branches

      ``-c, --create``: Create remote branch even if source does not exist

      ``-f, --force``: Force rename over existing branches

      ``-d, --dry-run``: If set, commands will be printed but not executed
