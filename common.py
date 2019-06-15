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


def run(usage, add_arguments, main):
    if '-h' in sys.argv:
        print(USAGE)
        print()

    parser = argparse.ArgumentParser()
    add_arguments(parser)
    parser.add_argument(
        '-c',
        '--commit-count',
        default=4,
        help='Number of commits per branch to show',
        type=int,
    )

    # Special case to handle -# arguments
    argv = []
    for i in sys.argv[1:]:
        if i.startswith('-') and i[1:].isnumeric():
            argv.extend(('-c', i[1:]))
        else:
            argv.append(i)

    args = parser.parse_args(argv)
    main(args)
