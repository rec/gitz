from pathlib import Path
import os
import shutil
import stat
import sys

COMMANDS = 'list', 'write'
PYTHON_HASH_BANG = '#!/usr/bin/env python'
BASE = Path('single_file/')
EXECUTABLE = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH


def _copy_python(source, target):
    gitz_begin = gitz_end = False
    gitz_lines = list(open('_gitz.py'))

    with open(target, 'w') as fp:
        for line in open(source):
            if gitz_end:
                fp.write(line)
            elif '_gitz' in line:
                gitz_begin = True
            elif gitz_begin:
                gitz_end = True
                fp.writelines(gitz_lines)
                fp.write('\n')
                fp.write('\n')
            else:
                fp.write(line)


def _is_python_file(filename):
    return next(open(filename)).startswith(PYTHON_HASH_BANG)


def main(command=None):
    if not command:
        raise ValueError('Missing command')

    if command not in COMMANDS:
        raise ValueError('No such command', command)

    files = (f for f in Path().iterdir() if f.name.startswith('git-'))
    if command == 'list':
        files = [f for f in files if _is_python_file(f)]
        files += [BASE / f.name for f in files]
        print(*files)
    else:
        for f in files:
            target = BASE / f.name
            if _is_python_file(f):
                _copy_python(f, target)
            else:
                shutil.copy2(f, target)
            st = f.stat()
            os.chown(target, st[stat.ST_UID], st[stat.ST_GID])
            os.chmod(target, st.st_mode)


if __name__ == '__main__':
    main(*sys.argv[1:])
