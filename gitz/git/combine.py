from . import GIT
import re
from typing import Union

COMMIT_MSG_RE = re.compile(r'\[.* ([0-9a-z]+)\] (.*)')


def combine(commits, squash: Union[None, str]):
    # Yields a stream of commit id, message
    symbol = '+' if squash is None else 's'

    def extract(lines):
        for line in lines:
            match = COMMIT_MSG_RE.match(line)
            if match:
                return match.groups()
        raise ValueError('Do not understand commit message' + lines[0])

    top = None

    for id in commits:
        commit_id, msg = extract(GIT.cherry_pick(id))
        top = top or commit_id
        yield symbol, commit_id, msg

    if squash is not None:
        GIT.reset('--soft', top)
        args = ['-m', squash] if squash else ['--no-edit']
        commit_id, msg = extract(GIT.commit('--amend', *args))
        yield '+', commit_id, msg


def permutation(perm):
    if len(perm) != len(set(perm)):
        raise ValueError('"%s" has repeating symbols' % perm)

    if not perm.isalpha():
        raise ValueError('Perm must be alphabetic')

    if not perm.islower():
        raise ValueError('Perm must be lowercase')

    result = [ord(i) - ord('a') for i in perm]
    result.append(max(result) + 1)
    return result


def clear_unchanged(perm):
    while perm:
        previous = -1 if len(perm) < 2 else perm[-2]
        if perm[-1] - previous == 1:
            perm.pop()
        else:
            break


def add_arguments(parser):
    parser.add_argument(
        '-s', '--squash', nargs='?', default=None, const='', help=_HELP_SQUASH
    )


_HELP_SQUASH = """Squash all commits into one.
If an argument is provided, use it as the commit message.
"""
