from .program import PROGRAM
from .runner import GIT

COMMIT_ID_LENGTH = 7


def _to_name(name):
    if isinstance(name, int):
        return 'HEAD~%d' % name
    if name.startswith('~'):
        return 'HEAD' + name
    if name.isnumeric() and len(name) < COMMIT_ID_LENGTH:
        return 'HEAD~' + name
    return name


def commit_id(name='HEAD', short=True):
    id = GIT('rev-parse', _to_name(name), info=True)[0]
    return id[:COMMIT_ID_LENGTH] if short else id


def commit_ids(names, short=True):
    names = (_to_name(n) for n in names)
    ids = GIT('rev-parse', *names, info=True)
    return [i[:COMMIT_ID_LENGTH] for i in ids] if short else ids


def commit_message(name='HEAD', short=True):
    cid = commit_id(name, short)
    message = GIT('show-branch', '--no-name', cid, info=True)[0]
    return '%s: %s' % (cid, message)


def fetch(remote):
    fetched = GIT.fetch(remote, info=True)
    while fetched and not fetched.startswith('From '):
        fetched.pop(0)
    if fetched:
        for f in fetched:
            PROGRAM.message(f)


def branch_name(name='HEAD'):
    lines = GIT('symbolic-ref', '-q', '--short', _to_name(name), info=True)
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
        remote, branch = rb.split('/')
        result.setdefault(remote, []).append(branch)
    return result


def upstream_remote(branch=None):
    # https://stackoverflow.com/a/9753364/43839
    upstream = 'rev-parse --abbrev-ref --symbolic-full-name %s@{u}'
    cmd = (upstream % (branch or '')).split()
    lines = GIT(*cmd, info=True, quiet=True)
    return lines[0].split('/', maxsplit=1)[0]


def force_flags(force=None):
    if force is None:
        force = PROGRAM.args.force
    return ['--force-with-lease'] if force else []
