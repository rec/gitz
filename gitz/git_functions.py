from . import util
from .program import PROGRAM


def commit_id(name='HEAD'):
    return PROGRAM.hidden.git('rev-parse', name)[0]


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
    return PROGRAM.hidden.git('symbolic-ref', '--short', name)[0].strip()


def is_workspace_dirty():
    if not util.find_git_root():
        return False
    try:
        PROGRAM.hidden.git('diff-index', '--quiet', 'HEAD', '--')
    except Exception:
        # Also returns true if workspace is broken for some other reason
        return True


def branches(*args):
    return PROGRAM.hidden.git.branch('--format=%(refname:short)', *args)


def all_branches(fetch=True):
    remotes = PROGRAM.hidden.git.remote()
    if fetch:
        for remote in remotes:
            PROGRAM.hidden.git.fetch(remote)
    result = {}
    for rb in branches('-r'):
        remote, branch = rb.split('/')
        result.setdefault(remote, []).append(branch)
    return result


def upstream_branch():
    # https://stackoverflow.com/a/9753364/43839
    g = PROGRAM.hidden.git(
        'rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}',
    )
    return g[0].split('/')
