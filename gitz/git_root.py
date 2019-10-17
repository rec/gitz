from . program import PROGRAM
from .runner import GIT
from pathlib import Path


def git_root(p='.'):
    p = Path(p).absolute()
    while not (p / '.git' / 'config').exists():
        if p.parent == p:
            return None
        p = p.parent
    return p


def check_git():
    if not git_root():
        PROGRAM.exit(_ERROR_NOT_GIT_REPOSITORY)


def is_workspace_dirty():
    if not git_root():
        return False
    try:
        GIT('diff-index', '--quiet', 'HEAD', '--', info=True)
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
