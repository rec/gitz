from . import guess_origin
from . import git_functions
from .program import PROGRAM
from .runner import GIT


def delete(branches):
    """Delete locally and upstream"""
    if not branches:
        PROGRAM.message('No branches specified')
        return

    try:
        origin = guess_origin.guess_origin()
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
        GIT.checkout(min(remaining_branches), quiet=True)

    deleted_count = 0
    PROGRAM.message('Deleted:')
    for b in branches:
        try:
            upstream = guess_origin.guess_origin(branch=b)
        except Exception:
            upstream = origin
        if upstream and b in remote_branches[upstream]:
            branch_name = '%s/%s' % (upstream, b)
            cid = git_functions.commit_id(branch_name)
            GIT.push(upstream, '--delete', b, quiet=True)
            PROGRAM.message('  %s: %s' % (cid, branch_name))
            deleted_count += 1

    local_branches = [b for b in branches if b not in unknown]

    if local_branches:
        locals_cid = git_functions.commit_ids(local_branches)

        GIT.branch('-D', *local_branches, quiet=True)
        for branch, cid in zip(local_branches, locals_cid):
            PROGRAM.message('  %s: %s' % (cid, branch))
            deleted_count += 1

    return deleted_count
