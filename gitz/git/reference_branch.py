from . import functions
from ..program import ARGS
from ..program import ENV
from ..program import PROGRAM


def reference_branch(remote_branches=None):
    remote_branches = remote_branches or functions.remote_branches()

    remote, *rest = ARGS.reference_branch.split('/', maxsplit=1)
    if rest:
        if remote not in remote_branches:
            PROGRAM.exit('Unknown remote', remote)

        branch = rest[0]
        if branch not in remote_branches[remote]:
            PROGRAM.exit(
                'Unknown reference branch', branch, 'in remote', remote
            )
        return remote, branch

    branches = [remote] if remote else ENV.reference_branches()
    if len(remote_branches) == 1:
        remotes = remote_branches
    else:
        remotes = [r for r in ENV.upstream() if r in remote_branches]

    for remote in remotes:
        for branch in branches:
            if branch in remote_branches[remote]:
                return remote, branch

    PROGRAM.exit('Cannot determine upstream remote')


def add_arguments(parser):
    parser.add_argument(
        '-r', '--reference-branch', default='', help=_HELP_REFERENCE_BRANCH
    )


_HELP_REFERENCE_BRANCH = (
    'Branch to create from, in the form ``branch`` or ``remote/branch``'
)
