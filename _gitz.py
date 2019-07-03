from pathlib import Path
import argparse
import contextlib
import functools
import os
import shlex
import subprocess
import sys


class Git:
    def __init__(self, verbose=None):
        if verbose is None:
            self.verbose = any(a in ('-v', '--verbose') for a in sys.argv)
        else:
            self.verbose = verbose

    def __getattr__(self, command):
        return functools.partial(self.git, command)

    def __call__(self, *cmd, **kwds):
        return git(*cmd, verbose=self.verbose, **kwds)

    def git(self, *cmd, **kwds):
        return self(*cmd, **kwds)

    def is_workspace_dirty(self):
        try:
            git('diff-index', '--quiet', 'HEAD', '--')
        except Exception:
            # Also returns true if the workspace is broken for some other reason
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
        return git('symbolic-ref', '--short', 'HEAD')[0].strip()

    def commit_id(self, name='HEAD', **kwds):
        return git('rev-parse', name, **kwds)[0].strip()

    def is_root(self, p):
        return (p / '.git' / 'config').exists()

    def _git(self, *cmd, **kwds):
        return run('git', *cmd, **kwds)


GIT = Git()

_SUBPROCESS_KWDS = {'encoding': 'utf-8', 'shell': True}


def git(*cmd, verbose=False, **kwds):
    if verbose:
        print('$ git', *cmd)
    lines = run('git', *cmd, **kwds)
    if verbose:
        print(*lines, sep='')
    return lines


def run(*cmd, **kwds):
    kwds = dict(_SUBPROCESS_KWDS, **kwds)
    if kwds.get('shell'):
        cmd = ' '.join(shlex.quote(c) for c in cmd)
    return subprocess.check_output(cmd, **kwds).splitlines()


def normalize(f):
    return os.path.expandvars(os.path.expanduser(f))


def chdir(f):
    os.chdir(normalize(f))


def get_argv():
    return ['-h' if i == '--help' else i for i in sys.argv[1:]]


def print_help(argv, usage=None):
    argv[:] = ['-h' if i == '--help' else i for i in argv]
    if '-h' in argv:
        usage and print(usage)
        print()
        return True


def run_argv(usage, main):
    argv = get_argv()
    if not print_help(argv, usage):
        main(*argv)


class Exit:
    def __init__(self, usage='', code=-1):
        self.usage = usage
        self.code = code

    def error_and_exit(self, *messages):
        self.error(*messages)
        self.print_usage()
        self.exit()

    def exit(self):
        sys.exit(self.code)

    def print_usage(self):
        if self.usage:
            print(self.usage, file=sys.stderr)

    def error(self, *messages):
        executable = Path(sys.argv[0]).name
        print('ERROR:', executable + ':', *messages, file=sys.stderr)


class CommitIndexer:
    COMMIT_ID_LENGTH = 6

    def __init__(self):
        self.commit_ids = [GIT.commit_id()]

    def index(self, commit_id):
        if commit_id.isnumeric() and len(commit_id) < self.COMMIT_ID_LENGTH:
            commit_id = 'HEAD~' + commit_id

        commit_id = GIT.commit_id(commit_id, stderr=subprocess.PIPE)
        for i, id in enumerate(self.commit_ids):
            if id.startswith(commit_id) or commit_id.startswith(id):
                return i

        commits = '%s~..%s~' % (commit_id, self.commit_ids[-1])
        for line in GIT.log('--oneline', commits, stderr=subprocess.PIPE):
            if line.strip():
                commit, *_ = line.split(maxsplit=1)
                self.commit_ids.append(commit.lower())
        return len(self.commit_ids) - 1
