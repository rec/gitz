from . import git_functions
from .program import PROGRAM
from .program import git


def combine(args, *commit_ids):
    git_functions.check_clean_workspace()
    ids, errors = [], []
    for id in commit_ids:
        try:
            ids.append(git_functions.commit_id(id))
        except Exception:
            errors.append(id)

    if errors:
        PROGRAM.exit('Not commit IDs:', *errors)

    base, *commits = ids

    result = []
    git.reset('--hard', base)
    if args.squash:
        for id in commits:
            git('cherry-pick', id)
        git.reset('--soft', base)
        git.commit('-m', args.squash)
        result = [git_functions.commit_id()]
    else:
        for id in commits:
            git('cherry-pick', id)
            result.append(git_functions.commit_id())

    return result


def shuffle(shuffle):
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
