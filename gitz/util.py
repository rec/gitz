from pathlib import Path
import os
import shlex
import subprocess

_SUBPROCESS_KWDS = {'encoding': 'utf-8', 'shell': True}
_EXCEPTION_MSG = 'Encountered an exception while executing'


def run(*cmd, use_shlex=False, verbose=False, **kwds):
    if verbose:
        print('$', *cmd)
    kwds = dict(_SUBPROCESS_KWDS, **kwds)
    cmd_str = ' '.join(cmd)

    if kwds.get('shell'):
        if use_shlex:
            cmd = (shlex.quote(c) for c in cmd)
        cmd = cmd_str

    try:
        lines = subprocess.check_output(cmd, **kwds).splitlines()
    except Exception as e:
        e.args = (_EXCEPTION_MSG, cmd_str) + e.args
        raise

    if verbose:
        print(*lines, sep='\n')
    return lines


def expand_path(s):
    return Path(os.path.expandvars(s)).expanduser().resolve()


def find_git_root(p='.'):
    p = Path(p)
    while not (p / '.git' / 'config').exists():
        if p.parent == p:
            return None
        p = p.parent
    return p
