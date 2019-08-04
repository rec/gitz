from . import util
from .program import PROGRAM

COMMIT_ID_LENGTH = 7


def commit_id(name='HEAD'):
    return PROGRAM.git('rev-parse', name)[0]


def exists(name):
    try:
        return commit_id(name)
    except Exception:
        return


def check_commit_id(name, program):
    try:
        return commit_id(name)
    except Exception:
        program.error_and_exit('Cannot resolve "%s" to a commit ID' % name)


def branch_name(name='HEAD'):
    return PROGRAM.git('symbolic-ref', '--short', name)[0].strip()


def is_workspace_dirty():
    if not util.find_git_root():
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
