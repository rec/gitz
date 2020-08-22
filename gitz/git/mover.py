from . import GIT
from . import functions
from . import root
from ..program import ARGS
from ..program import ENV
from ..program import PROGRAM

ACTIONS = {'copy': ('copi', 'over'), 'rename': ('renam', 'from or two')}


class Mover:
    """Moves things around, either with rename or copy"""

    def __init__(self, action):
        self.action = action
        self.is_rename = action == 'rename'
        self.word_root, self.direction = ACTIONS[action]
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

        try:
            self.origin = functions.upstream_remote(self.source)
        except Exception:
            self.origin = None

        self._check_branches()
        self._move_local()
        if self.origin:
            self._move_remote()

    def _check_branches(self):
        if self.source == self.target:
            PROGRAM.exit('Source and target must be different')

        branches = functions.branches()
        if self.source not in branches:
            PROGRAM.exit(_ERROR_LOCAL_REPO % self.source)

        if not ARGS.protected:
            p = ENV.protected_branches()
            if self.target in p:
                PROGRAM.exit(_ERROR_PROTECTED % (self.action, self.target))
            if self.is_rename and self.source in p:
                PROGRAM.exit(_ERROR_PROTECTED % (self.action, self.source))

        if ARGS.force:
            return

        if self.target in branches:
            PROGRAM.exit(_ERROR_TARGET_EXISTS % self.target)

        if not self.origin:
            return

        GIT.fetch(self.origin, info=True)
        ubranches = functions.remote_branches(False)[self.origin]
        if self.target in ubranches:
            PROGRAM.exit(_ERROR_TARGET_EXISTS % self.target)

    def _move_local(self):
        in_source = self.starting_branch == self.source
        in_target = self.starting_branch == self.target

        if in_source or in_target:
            root.check_clean_workspace()

        flag = '-C' if ARGS.force else '-c'

        if in_target:
            GIT.checkout(self.source)

        GIT.branch(flag, self.source, self.target)

        if self.is_rename:
            if in_source or in_target:
                GIT.checkout(self.target)
            GIT.branch('-D', self.source)

        if in_target:
            GIT.checkout(self.target)
        msg = '{0.Word_root}ed {0.source} -> {0.target} [{1}]'
        cid = functions.commit_id(self.target)
        PROGRAM.message(msg.format(self, cid))

    def _move_remote(self):
        rs = 'refs/remotes/{origin}/{source}:refs/heads/{target}'
        refspec = rs.format(**vars(self))
        GIT.push(self.origin, refspec, *functions.force_flags())
        if self.is_rename:
            GIT.push(self.origin, ':' + self.source)

        target = '%s/%s' % (self.origin, self.target)
        GIT.branch('-u', target, self.target)
        msg = '{0.Word_root}ed {0.origin}/{0.source} -> {1} [{2}]'
        cid = functions.commit_id(target)
        PROGRAM.message(msg.format(self, target, cid))

    def add_arguments(self, parser):
        add_arg = parser.add_argument
        add_arg('source')
        add_arg('target', nargs='?', default='')

        for f, h in BOOLEAN_FLAGS.items():
            args = [f] if f == 'protected' else [f[1:3], f]
            add_arg(*args, action='store_true', help=h.format(self))


DANGER = 'Changes remote branches!'
SUMMARY = '{0.Action} a git branch locally and remotely'
HELP = """
{0.Action} one branch to another, both locally and in remote
branches.  If no source branch is given, the current branch is
used.

By default, the branches `main`, `master` and `develop`, which means that they
are not allowed to be {0.word_root}ed {0.direction} to.

Using the --all/-a flag allows protected branches to be {0.word_root}ed.

It's also possible to override the protected branches by setting the
environment variable GITZ_PROTECTED_BRANCHES to a list separated by colons,
or an empty string for no protection.
"""
EXAMPLES = """
git {0.action} old new
    {0.Action} the branch "old" to "new", both locally and the remote
    repository.

    Fails if "new" exists locally or in the remote repositories.

git {0.action} -a old new
git {0.action} --all old new
    {0.Action} the branch "old" to "new", both locally and on the
    remote repository, even protected branches or repositories.

    Fails if "new" exists locally or in the remote repositories.

git {0.action} -f old new
git {0.action} --force old new
    {0.Action} the branch "old" to "new", both locally and on the upstream
    remote repository.

    Overwrites "new" if it exists locally or in the remote repository.
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
_ERROR_PROTECTED = 'Cannot %s over protected branch: %s'
_ERROR_TARGET_EXISTS = 'Branch %s already exists'


BOOLEAN_FLAGS = {
    '--protected': """{0.Action} all, even protected remotes or branches \
(use -protected to override)""",
    '--force': 'Force {0.action} over existing branches',
}
