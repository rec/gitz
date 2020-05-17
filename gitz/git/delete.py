from . import GIT
from . import functions
from . import guess_origin
from ..program import PROGRAM


def delete_remote_branch(remote, branch):
    rbranch = '%s/%s' % (remote, branch)
    cid, cmsg = functions.commit_message(rbranch)
    GIT.push(remote, ':refs/heads/' + branch)
    PROGRAM.message('- %s@%s: %s' % (rbranch, cid, cmsg))


def delete_all(branches):
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

    existing_branches = set(functions.branches())
    unknown = set(branches).difference(existing_branches)

    remote_branches = functions.remote_branches()
    if unknown:
        remotes = remote_branches.get(origin, [])
        missing = unknown.difference(remotes)
        PROGRAM.error_if(sorted(missing), 'Non-existent')

    remaining_branches = existing_branches.difference(branches)
    if not remaining_branches:
        raise ValueError('This would delete all the branches')

    if functions.branch_name() in branches:
        GIT.checkout(min(remaining_branches))

    deleted_count = 0
    PROGRAM.message('Deleted:')
    for b in branches:
        try:
            upstream = guess_origin.guess_origin(branch=b)
        except Exception:
            upstream = origin
        if upstream and b in remote_branches[upstream]:
            delete_remote_branch(upstream, b)
            deleted_count += 1

    local_branches = [b for b in branches if b not in unknown]

    if local_branches:
        for branch in local_branches:
            cid, cmsg = functions.commit_message(branch)
            PROGRAM.message('- %s@%s: %s' % (branch, cid, cmsg))
            deleted_count += 1
        GIT.branch('-D', *local_branches)

    return deleted_count
