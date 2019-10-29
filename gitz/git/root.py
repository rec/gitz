from ..program import PROGRAM
from ..program import GIT
from pathlib import Path
import os


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
    os.chdir(check_git())


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