from . import git_functions
from .program import PROGRAM
from .program import quiet_git


def delete(branches):
    """Delete locally and upstream"""
    if not branches:
        PROGRAM.message('No branches specified')
        return

    try:
        origin = git_functions.upstream_branch()[0]
    except Exception:
        origin = ''

    deduped, dupes = [], []
    for b in branches:
        (deduped, dupes)[b in deduped].append(b)

    if dupes:
        PROGRAM.error('Duplicate:', dupes)

    branches = deduped

    existing_branches = set(git_functions.branches())
    unknown = set(branches).difference(existing_branches)

    remote_branches = git_functions.remote_branches()
    if unknown:
        remotes = remote_branches.get(origin, [])
        missing = unknown.difference(remotes)
        PROGRAM.error_if(sorted(missing), 'Non-existent')

    remaining_branches = existing_branches.difference(branches)
    if not remaining_branches:
        raise ValueError('This would delete all the branches')

    if git_functions.branch_name() in branches:
        quiet_git.checkout(sorted(remaining_branches)[0])

    deleted_count = 0
    PROGRAM.message('Deleting:')
    for b in branches:
        try:
            upstream = git_functions.upstream_branch(b)[0]
        except Exception:
            upstream = origin
        if upstream and b in remote_branches[upstream]:
            branch_name = '%s/%s' % (upstream, b)
            cid = git_functions.commit_id(branch_name, True)
            quiet_git.push(upstream, '--delete', b)
            PROGRAM.message('  %s: %s' % (cid, branch_name))
            deleted_count += 1

    local_branches = [b for b in branches if b not in unknown]

    if local_branches:
        locals_cid = [git_functions.commit_id(b, True) for b in local_branches]
        quiet_git.branch('-D', *local_branches)
        for branch, cid in zip(local_branches, locals_cid):
            PROGRAM.message('  %s: %s' % (cid, branch))
            deleted_count += 1

    return deleted_count
