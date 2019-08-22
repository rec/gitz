from .program import PROGRAM
from pathlib import Path

COMMIT_ID_LENGTH = 7


def find_git_root(p='.'):
    p = Path(p)
    while not (p / '.git' / 'config').exists():
        if p.parent == p:
            return None
        p = p.parent
    return p


def commit_id(name='HEAD', short=False):
    try:
        if name.isnumeric() and len(name) < COMMIT_ID_LENGTH:
            name = 'HEAD~' + name
        id = PROGRAM.git('rev-parse', name)[0]
        if short:
            return id[:COMMIT_ID_LENGTH]
        return id

    except Exception:
        return


def branch_name(name='HEAD'):
    return PROGRAM.git('symbolic-ref', '-q', '--short', name)[0].strip()


def is_workspace_dirty():
    if not find_git_root():
        return False
    try:
        PROGRAM.git('diff-index', '--quiet', 'HEAD', '--')
    except Exception:
        # Also returns true if workspace is broken for some other reason
        return True


def branches(*args):
    return PROGRAM.git.branch('--format=%(refname:short)', *args)


def all_branches(fetch=True):
    remotes = PROGRAM.git.remote()
    if fetch:
        for remote in remotes:
            PROGRAM.git.fetch(remote)
    result = {}
    for rb in branches('-r'):
        remote, branch = rb.split('/')
        result.setdefault(remote, []).append(branch)
    return result


def upstream_branch():
    # https://stackoverflow.com/a/9753364/43839
    g = PROGRAM.git(
        'rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}'
    )
    return g[0].split('/')


def check_git():
    if not find_git_root():
        PROGRAM.error(_ERROR_NOT_GIT_REPOSITORY)
        PROGRAM.exit()


def check_clean_workspace():
    check_git()
    if is_workspace_dirty():
        PROGRAM.error(_ERROR_CHANGES_OVERWRITTEN)
        PROGRAM.exit()


_ERROR_CHANGES_OVERWRITTEN = 'Your local changes would be overwritten'
_ERROR_NOT_GIT_REPOSITORY = (
    'fatal: not a git repository (or any of the parent directories): .git'
)
