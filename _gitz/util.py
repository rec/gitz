from pathlib import Path
import os
import shlex
import subprocess

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


def expand_path(s):
    return Path(os.path.expandvars(s)).expanduser().resolve()
