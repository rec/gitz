from . import git_functions
from .program import PROGRAM
from .program import git


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

        if missing:
            brs = 'branch' if len(missing) == 1 else 'branches'
            miss = ', '.join(sorted(missing))
            PROGRAM.error('Non-existent', brs, miss)
    else:
        missing = set()

    remaining_branches = existing_branches.difference(branches)
    if not remaining_branches:
        raise ValueError('This would delete all the branches')

    if git_functions.branch_name() in branches:
        git.checkout(sorted(remaining_branches)[0])

    remotes_deleted = []
    for b in branches:
        try:
            upstream = git_functions.upstream_branch(b)[0]
        except Exception:
            upstream = origin
        if upstream and b in remote_branches[upstream]:
            git.push(upstream, '--delete', b)
            remotes_deleted.append('%s/%s' % (upstream, b))

    local_branches = [b for b in branches if b not in unknown]
    if local_branches:
        git.branch('-D', *local_branches)
    return local_branches + remotes_deleted
