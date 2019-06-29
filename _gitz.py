from pathlib import Path
import argparse
import contextlib
import os
import subprocess
import sys


def verbose():
    return any(a in ('-v', '--verbose') for a in sys.argv)


def git(*cmd, **kwds):
    cmd = ('git',) + cmd
    if verbose():
        print('$', *cmd)
    out = subprocess.check_output(('git',) + cmd, **kwds)
    lines = out.decode('utf-8').splitlines()
    return (i for i in lines if i.strip())


def is_git_dir(p):
    return (p / '.git' / config).exists()


def is_clean_workspace():
    try:
        return git('diff-index', '--quiet', 'HEAD', '--') or True
    except Exception:
        return False


def find_git_root(p):
    while not is_git_dir(p):
        if p.parent == p:
            return None
        p = p.parent
    return p


def cd_git_root():
    os.chdir(find_git_root(Path()))


def branches():
    return [b.strip().replace('* ', '') for b in git('branch')]


def current_branch():
    return next(git('symbolic-ref', '--short', 'HEAD')).strip()


def current_commit_id():
    return next(git('rev-parse', 'HEAD')).strip()


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
    def __init__(self, usage=None, code=-1):
        self.usage = usage
        self.code = code

    def exit(self, *messages):
        executable = Path(sys.argv[0]).name
        print('ERROR:', executable + ':', *messages, file=sys.stderr)
        if self.usage:
            print(self.usage, file=sys.stderr)
        sys.exit(self.code)

    @contextlib.contextmanager
    def on_exception(self, message):
        try:
            yield
        except Exception as exception:
            self.exit(message.format(**locals()))


@contextlib.contextmanager
def undo(function, before, after):
    function(before)
    try:
        yield
    finally:
        function(after)

"""
with undo(os.chdir, d, os.getcwd()):
    pass
with undo(lambda d: _gitz.git('checkout', d), d, os.getcwd()):
    pass
"""
