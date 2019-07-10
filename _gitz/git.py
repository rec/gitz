from pathlib import Path
import functools
import os
import subprocess
import sys
from .util import run

PROTECTED_BRANCHES_ENV_VARIABLE_NAME = 'GITZ_PROTECTED_BRANCHES'
PROTECTED_REMOTES_ENV_VARIABLE_NAME = 'GITZ_PROTECTED_REMOTES'
_PROTECTED_BRANCHES = 'master:develop'
_PROTECTED_REMOTES = 'upstream'


class Git:
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
        return run('git', *cmd, verbose=self.verbose, **kwds)

    def is_workspace_dirty(self):
        if not self.find_root():
            return False
        try:
            run('git', 'diff-index', '--quiet', 'HEAD', '--')
        except Exception:
            # Also returns true if workspace is broken for some other reason
            return True

    def find_root(self, p='.'):
        p = Path(p)
        while not self.is_root(p):
            if p.parent == p:
                return None
            p = p.parent
        return p

    def protected_branches(self):
        branches = os.environ.get(PROTECTED_BRANCHES_ENV_VARIABLE_NAME)
        return (branches or _PROTECTED_BRANCHES).split(':')

    def protected_remotes(self):
        remotes = os.environ.get(PROTECTED_REMOTES_ENV_VARIABLE_NAME)
        return (remotes or _PROTECTED_REMOTES).split(':')

    def remote_branches(self, unprotected=True):
        remotes = self.remotes()
        if unprotected:
            pr = self.protected_remotes()
            remotes = [r for r in remotes if r in pr]
        for remote in self.remotes:
            self.fetch(remote)

        result = {}
        for rb in self.branches('r'):
            remote, branch = rb.split('/')
            if remote in remotes:
                result.setdefault(remote, []).append(branch)
        return result

    def branches(self, *args):
        return self.branch('--format="%(refname:short)"', *args)

    def current_branch(self):
        return run('git', 'symbolic-ref', '--short', 'HEAD')[0].strip()

    def commit_id(self, name='HEAD', **kwds):
        return run('git', 'rev-parse', name, **kwds)[0].strip()

    def is_root(self, p):
        return (p / '.git' / 'config').exists()


GIT = Git()
GIT_SILENT = Git(stderr=subprocess.PIPE)
