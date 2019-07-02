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

    def git(self, *cmd, **kwds):
        return git(*cmd, verbose=self.verbose, **kwds)

    def is_workspace_dirty(self):
        try:
            git('diff-index', '--quiet', 'HEAD', '--')
        except Exception:
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

    def commit_id(self):
        return git('rev-parse', 'HEAD')[0].strip()

    def is_root(self, p):
        return (p / '.git' / 'config').exists()

    def _git(self, *cmd, **kwds):
        return run('git', *cmd, **kwds)


GIT = Git()

_SUBPROCESS_KWDS = {
    'encoding': 'utf-8',
    'shell': True,
}


def git(*cmd, verbose=False, **kwds):
    if verbose:
        print('$ git', *cmd)
    lines = git(*cmd, **kwds)
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

    def exit_if_help(self, argv=None):
        if argv is None:
            argv = sys.argv[1:]
        if any(a in ('-h', '--help') for a in argv):
            print(self.usage or '(no help available)', file=sys.stderr)
            sys.exit(0)

    def error_and_exit(self, *messages):
        self.print_error(*messages)
        self.print_usage()
        self.exit()

    def exit(self):
        sys.exit(self.code)

    def print_usage(self):
        if self.usage:
            print(self.usage, file=sys.stderr)

    def print_error(self, *messages):
        executable = Path(sys.argv[0]).name
        print('ERROR:', executable + ':', *messages, file=sys.stderr)
