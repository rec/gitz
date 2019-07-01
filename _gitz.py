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

    def git(self, *cmd, verbose=None, **kwds):
        if verbose is None:
            verbose = self.verbose
        if verbose:
            print('$ git', *cmd)
        lines = self._git(*cmd, **kwds)
        if verbose:
            print(*lines, sep='')
        return lines

    def is_workspace_dirty(self):
        try:
            self._git('diff-index', '--quiet', 'HEAD', '--')
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

    def checkout(self, *args):
        return self._git('checkout', '-q', *args)

    def current_branch(self):
        return self._git('symbolic-ref', '--short', 'HEAD')[0].strip()

    def commit_id(self):
        return self._git('rev-parse', 'HEAD')[0].strip()

    def is_root(self, p):
        return (p / '.git' / 'config').exists()

    def _git(self, *cmd, **kwds):
        return run('git', *cmd, **kwds)


GIT = Git()

_SUBPROCESS_KWDS = {
    'encoding': 'utf-8',
    'shell': True,
}


def run(*cmd, **kwds):
    kwds = dict(_SUBPROCESS_KWDS, **kwds)
    if kwds['shell']:
        cmd = ' '.join(cmd)
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


def numeric_flags(argv, flag):
    for i in argv:
        if i.startswith('-') and i[1:].isnumeric():
            yield flag
            yield i[1:]
        else:
            yield i


def commit_count(add_arguments, usage=None, commit_count=4):
    argv = get_argv()
    print_help(argv, usage)

    parser = argparse.ArgumentParser()
    add_arguments(parser)
    parser.add_argument(
        '-c',
        '--commit-count',
        default=commit_count,
        help='Number of commits per branch to show',
        type=int,
    )
    return parser.parse_args(list(numeric_flags(argv, '-c')))


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

    def exit(self, *messages, print_usage=True):
        if messages:
            self.error(*messages)
        if print_usage and self.usage:
            print(self.usage, file=sys.stderr)
        sys.exit(self.code)

    def error(self, *messages):
        executable = Path(sys.argv[0]).name
        print('ERROR:', executable + ':', *messages, file=sys.stderr)
