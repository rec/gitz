from . import GIT
from ..program import ARGS
from ..program import PROGRAM

COMMIT_ID_LENGTH = 7


def _to_name(name, base='HEAD'):
    if isinstance(name, int):
        return '%s~%d' % (base, name)
    if name.startswith('~'):
        return base + name
    if name.isnumeric() and len(name) < COMMIT_ID_LENGTH:
        return '%s~%s' % (base, name)
    return name


def commit_id(name='HEAD', short=True):
    id = GIT.rev_parse(_to_name(name), info=True)[0]
    return id[:COMMIT_ID_LENGTH] if short else id


def commit_ids(names, short=True):
    names = (_to_name(n) for n in names)
    ids = GIT.rev_parse(*names, info=True)
    return [i[:COMMIT_ID_LENGTH] for i in ids] if short else ids


def message(name='HEAD'):
    # TODO: this is a misleading name
    return GIT.show_branch('--no-name', _to_name(name), info=True)[0]


def commit_message(name='HEAD', short=True):
    # TODO: this is a misleading name
    return commit_id(name, short), message(name)


def commit_messages(count):
    return [commit_message(i) for i in range(count)]


def fetch(remote):
    fetched = GIT.fetch(remote, info=True)
    while fetched and not fetched.startswith('From '):
        fetched.pop(0)
    if fetched:
        for f in fetched:
            PROGRAM.message(f)


def branch_name(name='HEAD'):
    lines = GIT.symbolic_ref('-q', '--short', _to_name(name), info=True)
    return lines[0].strip()


def branches(*args):
    return GIT.branch('--format=%(refname:short)', *args, info=True)


def remote_branches(must_fetch=True):
    remotes = GIT.remote(info=True)

    if must_fetch:
        for remote in remotes:
            fetch(remote)

    result = {}
    for rb in branches('-r'):
        remote, branch = rb.split('/', maxsplit=1)
        result.setdefault(remote, []).append(branch)
    return result


def is_ancestor(parent, child='HEAD'):
    try:
        GIT.merge_base('--is-ancestor', parent, child)
        return True
    except Exception:
        return False


def check_is_ancestor(parent, child='HEAD'):
    if not is_ancestor(parent, child):
        PROGRAM.exit(parent, 'is not an ancestor of', child)


def upstream_remote(branch=None):
    # https://stackoverflow.com/a/9753364/43839
    upstream = 'rev-parse --abbrev-ref --symbolic-full-name %s@{u}'

    cmd = (upstream % (branch or '')).split()
    try:
        lines = GIT(*cmd, info=True)
    except ValueError:
        return  # No upstream remote
    return lines[0].split('/', maxsplit=1)[0]


def force_flags(force=None):
    if force is None:
        force = ARGS.force
    return ['--force-with-lease'] if force else []
