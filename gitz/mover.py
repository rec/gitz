from . import git_functions
from .env import ENV
from .program import PROGRAM
from .program import git


class Mover:
    """Moves things around, either with rename or copy"""

    def __init__(self, action):
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
        starting_branch = git_functions.branch_name()
        source = PROGRAM.args.source
        if PROGRAM.args.target:
            self.source, self.target = source, PROGRAM.args.target
        else:
            self.source, self.target = starting_branch, source

        self._get_remotes()
        self._check_branches()
        self._check_consistent()

        if PROGRAM.called['error']:
            PROGRAM.exit()

        self._move_local()
        self._move_remote()

        if starting_branch != self.source:
            git.checkout(self.starting_branch)

    def _move_local(self):
        flag = '-c' if self.action == 'copy' else '-m'
        flag = flag.upper() if PROGRAM.args.force else flag
        git.branch(flag, self.source, self.target)
        print(self.Root + 'ed', self.source, 'to', self.target)

    def _move_remote(self):
        git.checkout(self.target)
        force = git_functions.force_flags()
        for remote in self.old + self.new:
            git.push(*force, remote, self.target)

        if self.action != 'copy':
            for remote in self.old:
                git.push(remote, ':' + self.source)

    def _add_arguments(self, parser):
        add_arg = parser.add_argument
        add_arg('source')
        add_arg('target', nargs='?', default='')

        for f, h in BOOLEAN_FLAGS.items():
            add_arg(f[1:3], f, action='store_true', help=h.format(self))

    def _check_branches(self):
        pb = () if PROGRAM.args.all else ENV.protected_branches()
        branches = {self.target}
        if self.action != 'copy':
            branches.add(self.source)

        protected = branches.intersection(pb)
        if protected:
            self.error(_ERROR_PROTECTED_BRANCHES % ', '.join(protected))
            PROGRAM.exit()

        branches = git_functions.branches()
        if self.source not in branches:
            self.error(_ERROR_LOCAL_REPO % self.source)

        if not PROGRAM.args.force and self.target in branches:
            self.error(_ERROR_TARGET_EXISTS % self.target)

    def _get_remotes(self):
        remote_branches = git_functions.remote_branches()
        pr = () if PROGRAM.args.all else ENV.protected_remotes()
        remote_branches = {
            k: v for k, v in remote_branches.items() if k not in pr
        }

        self.old = []
        self.new = []
        for remote, branches in remote_branches.items():
            if self.target in branches and not PROGRAM.args.force:
                branch = remote + '/' + self.target
                self.error(_ERROR_TARGET_EXISTS % branch)
            elif self.source in branches:
                self.old.append(remote)
            elif PROGRAM.args.create:
                self.new.append(remote)

    def _check_consistent(self):
        if PROGRAM.args.force:
            return
        names = ('%s/%s' % (r, self.source) for r in self.old)
        commits = [git_functions.commit_id(n) for n in names]
        if len(set(commits)) > 1:
            commits = [c[: git_functions.COMMIT_ID_LENGTH] for c in commits]
            error = ' '.join('='.join(i) for i in zip(self.old, commits))
            self.error(_ERROR_INCONSISTENT_COMMITS, error)


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

git {0.action} -c old new
git {0.action} --create old new
    {0.Action} the branch "old" to "new", both locally and in remote
    repositories, even ones where the branch "old" does not exist

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
_ERROR_PROTECTED_BRANCHES = 'These branches are protected: %s'
_ERROR_TARGET_EXISTS = 'Branch %s already exists'


BOOLEAN_FLAGS = {
    '--all': '{0.Action} all, even protected remotes or branches',
    '--create': 'Create remote branch even if source does not exist',
    '--force': 'Force {0.action} over existing branches',
}
