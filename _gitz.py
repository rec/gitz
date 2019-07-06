from pathlib import Path
import argparse
import functools
import os
import shlex
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
        return run('git', *cmd, verbose=self.verbose, **kwds)

    def is_workspace_dirty(self):
        if not self.find_root():
            return False
        try:
            run('git', 'diff-index', '--quiet', 'HEAD', '--')
        except Exception:
            # Also returns true if workspace is broken for some other reason
            return True

    def find_root(self, p=Path()):
        while not self.is_root(p):
            if p.parent == p:
                return None
            p = p.parent
        return p

    def cd_root(self):
        root = self.find_root()
        if not root:
            raise ValueError('Working directory is not within a git directory')
        os.chdir(root)

    def branches(self):
        return [b.strip().replace('* ', '') for b in self.branch()]

    def current_branch(self):
        return run('git', 'symbolic-ref', '--short', 'HEAD')[0].strip()

    def commit_id(self, name='HEAD', **kwds):
        return run('git', 'rev-parse', name, **kwds)[0].strip()

    def is_root(self, p):
        return (p / '.git' / 'config').exists()


GIT = Git()
GIT_SILENT = Git(stderr=subprocess.PIPE)
_SUBPROCESS_KWDS = {'encoding': 'utf-8', 'shell': True}


def run(*cmd, use_shlex=False, verbose=False, **kwds):
    if verbose:
        print('$', *cmd)
    kwds = dict(_SUBPROCESS_KWDS, **kwds)
    if kwds.get('shell'):
        if use_shlex:
            cmd = (shlex.quote(c) for c in cmd)
        cmd = ' '.join(cmd)
    lines = subprocess.check_output(cmd, **kwds).splitlines()
    if verbose:
        print(*lines, sep='')
    return lines


class Program:
    def __init__(self, usage, help, code=-1):
        self.usage = usage
        self.help = help
        self.code = code
        self.program = Path(sys.argv[0]).name
        self.argv = sys.argv[1:]

    def exit_on_help(self):
        if self._print_help():
            sys.exit(0)

    def error_and_exit(self, *messages):
        self.error(*messages)
        print(self.usage, file=sys.stderr)
        self.exit()

    def exit(self):
        sys.exit(self.code)

    def error(self, *messages):
        print('ERROR:', self.program + ':', *messages, file=sys.stderr)

    def require_clean_workspace(self):
        if GIT.is_workspace_dirty():
            self.error('Your local changes would be overwritten')
            self.exit()

    def parse_args(self, add_arguments):
        self._print_help()
        parser = argparse.ArgumentParser()
        add_arguments(parser)
        return parser.parse_args(self.argv)

    def _print_help(self):
        if '-h' in self.argv or '--h' in self.argv:
            print(self.usage)
            print()
            print(self.help)
            return True


class CommitIndexer:
    def __init__(self):
        self.commit_ids = [GIT_SILENT.commit_id()]

    def index(self, commit_id):
        if commit_id.isnumeric() and len(commit_id) < COMMIT_ID_LENGTH:
            commit_id = 'HEAD~' + commit_id

        commit_id = GIT_SILENT.commit_id(commit_id)
        for i, id in enumerate(self.commit_ids):
            if id.startswith(commit_id) or commit_id.startswith(id):
                return i

        commits = '%s~..%s~' % (commit_id, self.commit_ids[-1])
        for line in GIT_SILENT.log('--oneline', commits):
            if line.strip():
                commit, *_ = line.split(maxsplit=1)
                self.commit_ids.append(commit.lower())
        return len(self.commit_ids) - 1
