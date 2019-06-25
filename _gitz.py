import argparse
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


def cd_git_root():
    cwd = os.getcwd()
    while not os.path.isdir('.git'):
        parent = os.path.dirname(os.getcwd())
        if parent == os.getcwd():
            os.chdir(cwd)
            raise ValueError('Not a git directory: %s' % cwd)
        os.chdir(parent)


def clean_workspace():
    try:
        return git('diff-index', '--quiet', 'HEAD', '--') or True
    except Exception:
        return False


def branches():
    return [b.strip().replace('* ', '') for b in git('branch')]


def current_branch():
    return next(git('symbolic-ref', '--short', 'HEAD')).strip()


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
