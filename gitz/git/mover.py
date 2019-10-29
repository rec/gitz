from . import functions
from . import root
from . import guess_origin
from ..program import ENV
from ..program import ARGS
from ..program import PROGRAM
from ..program import GIT

COPY, RENAME = 'copy', 'rename'


class Mover:
    """Moves things around, either with rename or copy"""

    def __init__(self, action):
        assert action in (RENAME, COPY)

        self.action = action
        if action == COPY:
            self.word_root = 'copi'
            self.direction = 'over'
        else:
            self.word_root = 'renam'
            self.direction = 'from or to'

        self.Action = self.action.capitalize()
        self.Word_root = self.word_root.capitalize()

        self.error = PROGRAM.error
        for k, v in NAMES.items():
            setattr(self, k, v.format(self))

    def __call__(self):
        keys = tuple(NAMES) + ('add_arguments', 'main')
        PROGRAM.start({k: getattr(self, k) for k in keys})

    def main(self):
        source = ARGS.source
        self.starting_branch = functions.branch_name()

        if ARGS.target:
            self.source, self.target = source, ARGS.target
        else:
            self.source, self.target = self.starting_branch, source

        if self.source == self.target:
            PROGRAM.exit('Source and target must be different')

        self._check_branches()
        self._move_local()
        self._move_remote()

    def _check_branches(self):
        branches = functions.branches()
        if self.source not in branches:
            PROGRAM.exit(_ERROR_LOCAL_REPO % self.source)

        self.origin = guess_origin.guess_origin(branch=self.source)

        if not ARGS.all:
            p = ENV.protected_branches()
            if self.target in p:
                PROGRAM.exit(_ERROR_PROTECTED_BRANCHES % self.target)
            if self.action == RENAME and self.source in p:
                PROGRAM.exit(_ERROR_PROTECTED_BRANCHES % self.source)

        if not ARGS.force:
            if self.target in branches:
                PROGRAM.exit(_ERROR_TARGET_EXISTS % self.target)
            GIT.fetch(self.origin, info=True)
            ubranches = functions.remote_branches(False)[self.origin]
            if self.target in ubranches:
                PROGRAM.exit(_ERROR_TARGET_EXISTS % self.target)

    def _move_local(self):
        in_source = (self.starting_branch == self.source)
        in_target = (self.starting_branch == self.target)

        if in_source or in_target:
            root.check_clean_workspace()

        flag = '-C' if ARGS.force else '-c'
        if in_target:
            GIT.checkout(self.source)
        GIT.branch(flag, self.source, self.target)
        if self.action == RENAME:
            if in_source:
                GIT.checkout(self.target)
            GIT.branch('-D', self.source)

        if in_target:
            GIT.checkout(self.target)
        msg = '{0.Word_root}ed {0.source} -> {0.target} [{1}]'
        cid = functions.commit_id(self.target)
        PROGRAM.message(msg.format(self, cid))

    def _move_remote(self):
        fl = functions.force_flags()
        GIT.push(*fl, '--set-upstream', self.origin, self.target)

        if self.action == RENAME:
            GIT.push(self.origin, ':' + self.source)

        target = '%s/%s' % (self.origin, self.target)
        msg = '{0.Word_root}ed {0.origin}/{0.source} -> {1} [{2}]'
        cid = functions.commit_id(target)
        PROGRAM.message(msg.format(self, target, cid))

    def add_arguments(self, parser):
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
to be {0.word_root}ed {0.direction}.

Using the --all/-a flag allows protected branches and remotes
to be {0.word_root}ed.

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

NAMES = {
    'HELP': HELP,
    'SUMMARY': SUMMARY,
    'EXAMPLES': EXAMPLES,
    'DANGER': DANGER,
}

_ERROR_CANNOT_DELETE = 'Cannot delete remote'
_ERROR_INCONSISTENT_COMMITS = 'Inconsistent commits IDs'
_ERROR_LOCAL_REPO = 'Branch %s does not exist in the local repository'
_ERROR_PROTECTED_BRANCHES = 'Protected: %s'
_ERROR_TARGET_EXISTS = 'Branch %s already exists'


BOOLEAN_FLAGS = {
    '--all': '{0.Action} all, even protected remotes or branches',
    '--force': 'Force {0.action} over existing branches',
}