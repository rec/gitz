from . import git_functions
from .program import PROGRAM
from .program import git


def delete(branches):
    """Delete locally and upsteram"""
    if not branches:
        PROGRAM.message('No branches specified')
        return

    deduped, dupes = [], []
    for b in branches:
        (deduped, dupes)[b in deduped].append(b)

    if dupes:
        PROGRAM.error('Duplicate:', dupes)

    branches = deduped

    existing_branches = set(git_functions.branches())
    unknown = set(branches).difference(existing_branches)
    if unknown:
        raise ValueError('Unknown', *sorted(unknown))

    remaining_branches = existing_branches.difference(branches)
    if not remaining_branches:
        raise ValueError('This would delete all the branches')

    if git_functions.branch_name() in branches:
        git.checkout(sorted(remaining_branches)[0])

    for b in branches:
        upstream = git_functions.upstream_branch(b)[0]
        git.push(upstream, '--delete', b)

    git.branch('-D', *branches)
    return branches
