import pathlib
import sys


def make_single_file(name):
    pass


def list_python_files():
    files = []

    for f in pathlib.Path().iterdir():
        if f.name.startswith('git-'):
            if next(open(f)).startswith('#!/usr/bin/env python'):
                files.append(f)
    print(*files)


def main(args):
    if args:
        for name in args:
            make_single_file(name)
    else:
        list_python_files()


if __name__ == '__main__':
    main(sys.argv[1:])
