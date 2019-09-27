from . import git_functions
from .env import ENV
from .program import PROGRAM
from .program import safe_git
from .program import quiet_git

COPY, RENAME = 'copy', 'rename'


class Mover:
    """Moves things around, either with rename or copy"""

    def __init__(self, action):
        assert action in (RENAME, COPY)

        self.action = action
        if action == COPY:
            self.root = 'copi'
            self.direction = 'over'
        else:
            self.root = 'renam'
            self.direction = 'from or to'

        self.Action = self.action.capitalize()
        self.Root = self.root.capitalize()

        self.error = PROGRAM.error

    def __call__(self):
        PROGRAM.start(
            {
                'add_arguments': self._add_arguments,
                'HELP': HELP.format(self),
                'SUMMARY': SUMMARY.format(self),
                'EXAMPLES': EXAMPLES.format(self),
                'DANGER': DANGER.format(self),
                'main': self.run,
            }
        )

    def run(self):
        source = PROGRAM.args.source
        self.starting_branch = git_functions.branch_name()

        if PROGRAM.args.target:
            self.source, self.target = source, PROGRAM.args.target
        else:
            self.source, self.target = self.starting_branch, source

        self._check_branches()
        self._move_local()
        self._move_remote()

    def _check_branches(self):
        if self.source == self.target:
            PROGRAM.exit('Source and target must be different')

        self.in_source = self.starting_branch == self.source
        self.in_target = self.starting_branch == self.target
        if self.in_source or self.in_target:
            git_functions.check_clean_workspace()

        branches = git_functions.branches()
        if self.source not in branches:
            PROGRAM.exit(_ERROR_LOCAL_REPO % self.source)

        self.origin = git_functions.upstream_branch(self.source)[0]

        if not PROGRAM.args.all:
            p = ENV.protected_branches()
            if self.target in p:
                PROGRAM.exit(_ERROR_PROTECTED_BRANCHES % self.target)
            if self.action == RENAME and self.source in p:
                PROGRAM.exit(_ERROR_PROTECTED_BRANCHES % self.source)

        if not PROGRAM.args.force:
            if self.target in branches:
                PROGRAM.exit(_ERROR_TARGET_EXISTS % self.target)
            safe_git.fetch(self.origin)
            ubranches = git_functions.remote_branches(False)[self.origin]
            if self.target in ubranches:
                PROGRAM.exit(_ERROR_TARGET_EXISTS % self.target)

    def _move_local(self):
        flag = '-C' if PROGRAM.args.force else '-c'
        if self.in_target:
            quiet_git.checkout(self.source)
        quiet_git.branch(flag, self.source, self.target)
        if self.action == RENAME:
            if self.in_source:
                quiet_git.checkout(self.target)
            quiet_git.branch('-D', self.source)

        if self.in_target:
            quiet_git.checkout(self.target)
        PROGRAM.message('{Root}ed {source} -> {target}'.format(**vars(self)))

    def _move_remote(self):
        force = git_functions.force_flags()
        quiet_git.push(*force, '--set-upstream', self.origin, self.target)

        if self.action == RENAME:
            quiet_git.push(self.origin, ':' + self.source)

        msg = '{Root}ed {origin}/{source} -> {origin}/{target}'
        PROGRAM.message(msg.format(**vars(self)))

    def _add_arguments(self, parser):
        add_arg = parser.add_argument
        add_arg('source')
        add_arg('target', nargs='?', default='')

        for f, h in BOOLEAN_FLAGS.items():
            add_arg(f[1:3], f, action='store_true', help=h.format(self))


DANGER = 'Changes remote branches!'
SUMMARY = '{0.Action} a git branch locally and on all remotes'
HELP = """
{0.Action} one branch to another, both locally and in remote
branches.  If no source branch is given, the current branch is
used.

By default, the branches `master` and `develop` and the remote
`upstream` are protected, which means that they are not allowed
to be {0.root}ed {0.direction}.

Using the --all/-a flag allows protected branches and remotes
to be {0.root}ed.

It's also possible to override the protected branches or the
protected remotes by setting one of the environment variables
GITZ_PROTECTED_BRANCHES or GITZ_PROTECTED_REMOTES
to a list separated by colons, or an empty string for no protection.
"""
EXAMPLES = """
git {0.action} old new
    {0.Action} the branch "old" to "new", both locally and in remote
    repositories where the branch "old" exists.

    Fails if "new" exists locally or in the remote repositories.

git {0.action} -a old new
git {0.action} --all old new
    {0.Action} the branch "old" to "new", both locally and in remote
    repositories, even protected branches or repositories.

    Fails if "new" exists locally or in the remote repositories.

git {0.action} -f old new
git {0.action} --force old new
    {0.Action} the branch "old" to "new", both locally and in remote
    repositories where the branch "old" exists.

    Overwrites "new" if it exists locally or in the remote repositories.
"""

_ERROR_CANNOT_DELETE = 'Cannot delete remote'
_ERROR_INCONSISTENT_COMMITS = 'Inconsistent commits IDs'
_ERROR_LOCAL_REPO = 'Branch %s does not exist in the local repository'
_ERROR_PROTECTED_BRANCHES = 'Protected: %s'
_ERROR_TARGET_EXISTS = 'Branch %s already exists'


BOOLEAN_FLAGS = {
    '--all': '{0.Action} all, even protected remotes or branches',
    '--force': 'Force {0.action} over existing branches',
}
