from . import util
from .git import COMMIT_ID_LENGTH
from .git import GIT_SILENT


def commit_id(name='HEAD', git=GIT_SILENT):
    return git.git('rev-parse', name)[0].strip()[:COMMIT_ID_LENGTH]


def exists(name, git=GIT_SILENT):
    try:
        return commit_id(name, git)
    except Exception:
        return


def current_branch(name='HEAD', git=GIT_SILENT):
    return git.git('symbolic-ref', '--short', name)[0].strip()


def is_workspace_dirty(git=GIT_SILENT):
    if not util.find_git_root():
        return False
    try:
        git.git('diff-index', '--quiet', 'HEAD', '--')
    except Exception:
        # Also returns true if workspace is broken for some other reason
        return True


def branches(*args, git=GIT_SILENT):
    return git.branch('--format="%(refname:short)"', *args)


def all_branches(fetch=True, git=GIT_SILENT):
    remotes = git.remote()
    if fetch:
        for remote in remotes:
            git.fetch(remote)
    result = {}
    for rb in branches('-r', git=git):
        remote, branch = rb.split('/')
        result.setdefault(remote, []).append(branch)
    return result
