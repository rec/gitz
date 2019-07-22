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


def check_commit_id(name, program, git=GIT_SILENT):
    try:
        return commit_id(name, git)
    except Exception:
        program.error_and_exit('Cannot resolve "%s" to a commit ID' % name)


def branch_name(name='HEAD', git=GIT_SILENT):
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


def upstream_branch(git=GIT_SILENT):
    # https://stackoverflow.com/a/9753364/43839
    return git.git('rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}')


def delete(to_delete, program, remotes, git=GIT_SILENT):
    """Delete locally and on zero or more remotes"""
    br = branches()
    local_delete = [b for b in to_delete if b in br]
    if len(local_delete) == len(br):
        raise ValueError('This would delete all the branches')

    if branch_name() in local_delete:
        git.checkout(next(b for b in br if b not in local_delete))

    if local_delete:
        git.branch('-D', *local_delete)

    count = len(local_delete)
    remote_branches = all_branches(git=git)

    for remote in remotes:
        remote_delete = [b for b in to_delete if b in remote_branches[remote]]
        if remote_delete:
            git.push(remote, '--delete', *remote_delete)
            count += len(remote_delete)

    return count
