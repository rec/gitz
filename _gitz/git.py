import functools
import subprocess
import sys
from . import util


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

    def is_workspace_dirty(self):
        if not self.find_root():
            return False
        try:
            util.run('git', 'diff-index', '--quiet', 'HEAD', '--')
        except Exception:
            # Also returns true if workspace is broken for some other reason
            return True

    def all_branches(self, fetch=True):
        remotes = self.remotes()
        if fetch:
            for remote in remotes:
                self.fetch(remote)
        result = {}
        for rb in self.branches('r'):
            remote, branch = rb.split('/')
            result.setdefault(remote, []).append(branch)
        result[self.LOCAL] = self.branches()
        return result

    def branches(self, *args):
        return self.branch('--format="%(refname:short)"', *args)

    def current_branch(self, name='HEAD'):
        return util.run('git', 'symbolic-ref', '--short', name)[0].strip()

    def commit_id(self, name='HEAD'):
        return util.run('git', 'rev-parse', name)[0].strip()

    find_root = staticmethod(util.find_git_root)


GIT = Git()
GIT_SILENT = Git(stderr=subprocess.PIPE)
COMMIT_ID_LENGTH = 7
