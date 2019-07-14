from . import util
import functools
import subprocess
import sys

COMMIT_ID_LENGTH = 7


class Git:
    LOCAL = '/'
    """Artificial origin for branches on the local repo"""

    def __init__(self, verbose=None, **kwds):
        if verbose is None:
            self.verbose = any(a in ('-v', '--verbose') for a in sys.argv)
        else:
            self.verbose = verbose
        self.kwds = kwds

    def __getattr__(self, command):
        return functools.partial(self.git, command)

    def git(self, *cmd, **kwds):
        kwds = dict(self.kwds, **kwds) if self.kwds else kwds
        return util.run('git', *cmd, verbose=self.verbose, **kwds)


GIT = Git()
GIT_SILENT = Git(stderr=subprocess.PIPE)


def commit_id(name='HEAD'):
    return util.run('git', 'rev-parse', name)[0].strip()[:COMMIT_ID_LENGTH]


def current_branch(name='HEAD'):
    return util.run('git', 'symbolic-ref', '--short', name)[0].strip()


def is_workspace_dirty():
    if not util.find_git_root():
        return False
    try:
        util.run('git', 'diff-index', '--quiet', 'HEAD', '--')
    except Exception:
        # Also returns true if workspace is broken for some other reason
        return True


def branches(*args, git=GIT):
    return git.branch('--format="%(refname:short)"', *args)


def all_branches(fetch=True, git=GIT):
    # Currently unused
    remotes = git.remotes()
    if fetch:
        for remote in remotes:
            git.fetch(remote)
    result = {}
    for rb in branches('r', git=git):
        remote, branch = rb.split('/')
        result.setdefault(remote, []).append(branch)
    result[git.LOCAL] = branches(git=git)
    return result
