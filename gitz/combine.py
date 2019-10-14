from . import git_functions
from . import git_root
from .program import git


def combine(squash, *commit_ids):
    git_root.check_clean_workspace()
    ids, errors = [], []
    for id in commit_ids:
        try:
            ids.append(git_functions.commit_id(id))
        except Exception:
            errors.append(id)

    if errors:
        raise ValueError('Not commit IDs:', ' '.join(errors))

    base, *commits = ids

    result = []
    git.reset('--hard', base)
    if squash:
        for id in commits:
            git('cherry-pick', id)
        git.reset('--soft', base)
        git.commit('-m', squash)
        result = [git_functions.commit_id()]
    else:
        for id in commits:
            git('cherry-pick', id)
            result.append(git_functions.commit_id())

    return result


def shuffle(shuffle, squash=False):
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
    parser.add_argument('-s', '--squash', help=_HELP_SQUASH)


_HELP_SQUASH = 'Squash all commits into one, with a message'
