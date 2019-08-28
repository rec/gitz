``git-copy``: Copy a git branch locally and on all remotes
----------------------------------------------------------

USAGE
=====
.. code-block:: bash

    git copy [<source-branch>] <target-branch>

DANGER
======

    Changes remote branches!

DESCRIPTION
===========

    Copy one branch to another, both locally and in remote
    branches.  If no source branch is given, the current branch is
    used.
    
    By default, the branches `master` and `develop` and the remote
    `upstream` are protected, which means that they are not allowed
    to be copied over.
    
    Using the --all/-a flag allows protected branches and remotes
    to be copied.
    
    It's also possible to override the protected branches or the
    protected remotes by setting one of the environment variables
    GITZ_PROTECTED_BRANCHES or GITZ_PROTECTED_REMOTES
    to a list separated by colons, or an empty string for no protection.

EXAMPLES
========

    git copy old new
        Copy the branch "old" to "new", both locally and in remote
        branches.

FLAGS
=====

    Full usage: git-copy [-h] [-q] [-v] [-a] [-c] [-f] [-d] source [target]
    
    positional arguments:
      source
      target
    
    optional arguments:
      -h, --help     show this help message and exit
      -q, --quiet    Suppress all output
      -v, --verbose  Report all messages in great detail
      -a, --all      Copy all, even protected remotes or branches
      -c, --create   Create remote branch even if source does not exist
      -f, --force    Force copy over existing branches
      -d, --dry-run  If set, commands will be printed but not executed
