from . import git
from . import git_functions
from .env import ENV
from .git import GIT
from .program import PROGRAM


class Mover:
    """Moves things around, either with rename or copy"""

    def __init__(self, action, examples=''):
        assert action in ('rename', 'copy')

        self.action = action
        if action == 'copy':
            self.root = 'copi'
            self.direction = 'over'
        else:
            self.root = 'renam'
            self.direction = 'from or to'

        self.Action = self.action.capitalize()
        self.Root = self.root.capitalize()

        assert not (PROGRAM.help or PROGRAM.usage)
        PROGRAM.help = HELP.format(self) + examples
        PROGRAM.usage = USAGE.format(self)

        self.error = PROGRAM.error
        self.args = PROGRAM.parse_args(self._add_arguments)

    def __call__(self):
        starting_branch = git_functions.branch_name()
        source = self.args.source
        if self.args.target:
            self.source, self.target = source, self.args.target
        else:
            self.source, self.target = starting_branch, source

        self._get_remotes()
        self._check_branches()
        self._check_consistent()

        if PROGRAM.called.get('error'):
            PROGRAM.exit()

        self._move_local()
        self._move_remote()

        if starting_branch != self.source:
            git.checkout(self.starting_branch)

    def _move_local(self):
        flag = '-c' if self.action == 'copy' else '-m'
        flag = flag.upper() if self.args.force else flag
        GIT.branch(flag, self.source, self.target)
        print(self.Root + 'ed', self.source, 'to', self.target)

    def _move_remote(self):
        GIT.checkout(self.target)
        force = ['--force-with-lease'] if self.args.force else []
        for remote in self.old + self.new:
            GIT.push(*force, remote, self.target)

        if self.action != 'copy':
            for remote in self.old:
                GIT.push(remote, ':' + self.source)

    def _add_arguments(self, parser):
        add_arg = parser.add_argument
        add_arg('source')
        add_arg('target', nargs='?', default='')

        for f, h in BOOLEAN_FLAGS.items():
            add_arg(f, f[1:3], action='store_true', help=h.format(self))

    def _check_branches(self):
        pb = () if self.args.all else ENV.protected_branches()
        if any(i in pb for i in (self.source, self.target)):
            self.error(_ERROR_PROTECTED_BRANCHES % ':'.join(pb))
            PROGRAM.exit()

        branches = git_functions.branches()
        if self.source not in branches:
            self.error(_ERROR_LOCAL_REPO % self.source)

        if not self.args.force and self.target in branches:
            self.error(_ERROR_TARGET_EXISTS % self.target)

    def _get_remotes(self):
        all_branches = git_functions.all_branches()
        pr = () if self.args.all else ENV.protected_remotes()
        all_branches = {k: v for k, v in all_branches.items() if k not in pr}

        self.old = []
        self.new = []
        for remote, branches in all_branches.items():
            if self.target in branches and not self.args.force:
                branch = remote + '/' + self.target
                self.error(_ERROR_TARGET_EXISTS % branch)
            elif self.source in branches:
                self.old.append(remote)
            elif self.args.create:
                self.new.append(remote)

    def _check_consistent(self):
        if self.args.force:
            return
        names = ('%s/%s' % (r, self.source) for r in self.old)
        commits = [git_functions.commit_id(n) for n in names]
        if len(set(commits)) > 1:
            commits = [c[: git.COMMIT_ID_LENGTH] for c in commits]
            error = ' '.join('='.join(i) for i in zip(self.old, commits))
            self.error(_ERROR_INCONSISTENT_COMMITS, error)


USAGE = """\
git-{0.action}:
    {0.Root}es a git branch locally and on all remotes

USAGE:
    git {0.action} [<source-branch>] <target-branch>
"""

HELP = """
{0.Root}es one branch to another, both locally and in remote
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

_ERROR_CANNOT_DELETE = 'Cannot delete remote'
_ERROR_INCONSISTENT_COMMITS = 'Inconsistent commits IDs'
_ERROR_LOCAL_REPO = 'Branch %s does not exist in the local repository'
_ERROR_PROTECTED_BRANCHES = 'These branches are protected: %s'
_ERROR_TARGET_EXISTS = 'Branch %s already exists'


BOOLEAN_FLAGS = {
    '--all': '{0.Action} all, even protected remotes or branches',
    '--create': 'Create remote branch even if source does not exist',
    '--force': 'Force {0.action} over existing branches',
}
