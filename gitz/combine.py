from . import git_functions
from .runner import GIT


def combine(commits, squash):
    result = []
    for id in commits:
        GIT('cherry-pick', id)
        result.append(git_functions.commit_id())

    if squash is not None:
        GIT.reset('--soft', result[0])
        args = ['-m', squash] if squash else ['--no-edit']
        GIT.commit('--amend', *args)
        result = [git_functions.commit_id()]

    return result


def shuffle(shuffle, squash=None):
    shuffle = shuffle.replace('-', '_')
    names = shuffle.replace('_', '')
    sorted_names = sorted(names)

    if len(set(names)) < len(names):
        raise ValueError('"%s" has repeating symbols' % shuffle)

    result = []
    for name in names:
        i = sorted_names.index(name)
        result.append(shuffle.index(names[i]))

    result.append(len(shuffle))
    last = None
    unchanged = 0

    if not squash:
        while result and result[-1] == len(result) - 1:
            last = result.pop()
            unchanged += 1
        if result and last is not None:
            result.append(last)
            unchanged -= 1

    return result, unchanged if result else 0


def add_arguments(parser):
    parser.add_argument(
        '-s', '--squash', nargs='?', default=None, const='', help=_HELP_SQUASH
    )


_HELP_SQUASH = """Squash all commits into one.
If an argument is provided, use it as the commit message.
"""
