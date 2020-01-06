from . import GIT
import re

COMMIT_MSG_RE = re.compile(r'\[.* ([0-9a-z]+)\] (.*)')


def combine(commits, squash):
    # Yields a stream of commit id, message
    symbol = '+' if squash is None else 's'

    def extract(lines):
        match = COMMIT_MSG_RE.match(lines[0])
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


def shuffle(shuffle, squash=None):
    if len(shuffle) != len(set(shuffle)):
        raise ValueError('"%s" has repeating symbols' % shuffle)

    if shuffle.isnumeric():
        base = '0'

    elif not shuffle.isalpha():
        raise ValueError('Shuffle must be alphabetic')

    elif not shuffle.islower():
        raise ValueError('Shuffle must be lowercase')

    else:
        base = 'a'

    result = [ord(i) - ord(base) for i in shuffle]
    result.append(max(result) + 1)

    if squash is None:
        while result:
            previous = -1 if len(result) < 2 else result[-2]
            if result[-1] - previous == 1:
                result.pop()
            else:
                break

    return result


def add_arguments(parser):
    parser.add_argument(
        '-s', '--squash', nargs='?', default=None, const='', help=_HELP_SQUASH
    )


_HELP_SQUASH = """Squash all commits into one.
If an argument is provided, use it as the commit message.
"""
