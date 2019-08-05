from . import git_functions
from .program import PROGRAM
import contextlib


@contextlib.contextmanager
def reset_on_conflict(args):
    commit_id = git_functions.commit_id()
    try:
        yield
    except Exception as e:
        if not args.preserve_conflict:
            PROGRAM.git.reset('--hard', commit_id)
        PROGRAM.error_and_exit('In git:', e)


def add_conflict_arguments(parser):
    parser.add_argument(
        '-p',
        '--preserve-conflict',
        action='store_true',
        help='Do not revert the workspace on failure',
    )


def combine(args, *commit_ids):
    PROGRAM.check_clean_workspace()
    ids, errors = [], []
    for id in commit_ids:
        try:
            ids.append(git_functions.commit_id(id))
        except Exception:
            errors.append(id)

    if errors:
        PROGRAM.error_and_exit('Not commit IDs:', *errors)

    with reset_on_conflict(args):
        base, *commits = ids
        PROGRAM.git.reset('--hard', base)
        for id in commits:
            PROGRAM.git('cherry-pick', id)


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
    while result and result[-1] == len(result) - 1:
        result.pop()
    return result
