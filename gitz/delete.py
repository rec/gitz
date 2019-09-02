from . import git_functions
from .program import git
from .program import safe_git


def delete(branches, remotes):
    """Delete locally and on zero or more remotes"""
    # Locally
    existing_branches = git_functions.branches()
    to_delete = [b for b in branches if b in existing_branches]
    if len(to_delete) == len(existing_branches):
        raise ValueError('This would delete all the branches')

    unknown_remotes = set(remotes).difference(safe_git.remote())
    if unknown_remotes:
        raise ValueError('Unknown remotes:', *unknown_remotes)

    if git_functions.branch_name() in to_delete:
        undeleted_branch = next(b for b in branches if b not in to_delete)
        git.checkout(undeleted_branch)

    if to_delete:
        git.branch('-D', *to_delete)

    # Remote branches
    for remote in remotes:
        git_functions.fetch(remote)
        rb = git_functions.branches('-r')
        to_delete_remote = [b for b in branches if (remote + '/' + b) in rb]
        if to_delete_remote:
            git.push(remote, '--delete', *to_delete_remote)
            to_delete.extend('%s/%s' % (remote, i) for i in to_delete_remote)

    return to_delete
