import argparse
import contextlib
import os
import subprocess
import sys


def git(*cmd, **kwds):
    out = subprocess.check_output(('git',) + cmd, **kwds)
    lines = out.decode('utf-8').splitlines()
    return (i for i in lines if i.strip())


def cd_git_root():
    while not os.path.isdir('.git'):
        parent = os.path.dirname(os.getcwd())
        if parent == os.getcwd():
            raise ValueError('Not in a git directory')
        os.chdir(parent)


def clean_workspace():
    try:
        return git('diff-index', '--quiet', 'HEAD', '--') or True
    except Exception:
        return False


def get_argv():
    return ['-h' if i == '--help' else i for i in sys.argv[1:]]


def get_help(argv, usage=None):
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
    get_help(argv, usage)

    parser = argparse.ArgumentParser()
    add_arguments(parser)
    parser.add_argument(
        '-c',
        '--commit-count',
        default=commit_count,
        help='Number of commits per branch to show',
        type=int,
    )

    args = parser.parse_args(list(numeric_flags(argv, '-c')))
    return args


def branches():
    return [b.strip().replace('* ', '') for b in git('branch')]


def current_branch():
    return next(git('symbolic-ref', '--short', 'HEAD')).strip()
