from . import git_functions
from .program import PROGRAM


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
    PROGRAM.dry.git.reset('--hard', base)
    for id in commits:
        PROGRAM.dry.git('cherry-pick', id)


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
    while result and result[-1] == len(result) - 1:
        last = result.pop()
    if result and last is not None:
        result.append(last)

    return result
