from . import util
import functools
import subprocess
import sys

COMMIT_ID_LENGTH = 7


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
        return util.run('git', *cmd, verbose=self.verbose, **kwds)


GIT = Git()
GIT_SILENT = Git(stderr=subprocess.PIPE)
