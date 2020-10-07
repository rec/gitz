from . import GIT
from ..program import PROGRAM
from pathlib import Path
import functools
import os


# See https://stackoverflow.com/questions/957928
def root(p='.'):
    p = Path(p).absolute()
    while not (p / '.git' / 'config').exists():
        if p.parent == p:
            return None
        p = p.parent
    return p


def check_git():
    gr = root()
    if gr:
        return gr

    PROGRAM.exit(_ERROR_NOT_GIT_REPOSITORY)


def cd_root():
    os.chdir(str(check_git()))


def run_in_root(fn):
    @functools.wraps(fn)
    def wrapped(*args, **kwds):
        saved = os.getcwd()
        cd_root()
        try:
            return fn(*args, **kwds)
        finally:
            os.chdir(saved)

    return wrapped


def is_workspace_dirty():
    if not root():
        return False
    try:
        GIT.diff_index('--quiet', 'HEAD', '--', info=True)
    except Exception:
        # Also returns true if workspace is broken for some other reason
        return True


def check_clean_workspace():
    check_git()
    if is_workspace_dirty():
        PROGRAM.exit(_ERROR_CHANGES_OVERWRITTEN)


_ERROR_CHANGES_OVERWRITTEN = 'Your local changes would be overwritten'
_ERROR_NOT_GIT_REPOSITORY = (
    'fatal: not a git repository (or any of the parent directories): .git'
)
