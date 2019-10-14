from .program import PROGRAM
from .program import safe_git

COMMIT_ID_LENGTH = 7


def _to_name(name):
    if isinstance(name, int):
        return 'HEAD~%d' % name
    if name.startswith('~'):
        return 'HEAD' + name
    if name.isnumeric() and len(name) < COMMIT_ID_LENGTH:
        return 'HEAD~' + name
    return name


def commit_id(name='HEAD', short=False):
    try:
        id = safe_git('rev-parse', _to_name(name), quiet=True)[0]
        if short:
            return id[:COMMIT_ID_LENGTH]
        return id
    except Exception:
        return


def commit_ids(names):
    ids, errors = [], []
    for id in names:
        try:
            ids.append(commit_id(id))
        except Exception:
            errors.append(id)
    if errors:
        raise ValueError('Not commit IDs:', ' '.join(errors))
    return ids


def commit_message(name='HEAD'):
    cid = commit_id(name)
    if cid:
        message = safe_git('show-branch', '--no-name', cid)[0]
        return '%s: %s' % (cid[:COMMIT_ID_LENGTH], message)


def fetch(remote):
    fetched = safe_git.fetch(remote)
    while fetched and not fetched.startswith('From '):
        fetched.pop(0)
    if fetched:
        for f in fetched:
            PROGRAM.message(f)


def branch_name(name='HEAD'):
    return safe_git('symbolic-ref', '-q', '--short', _to_name(name))[0].strip()


def branches(*args):
    return safe_git.branch('--format=%(refname:short)', *args)


def remote_branches(must_fetch=True):
    remotes = safe_git.remote()

    if must_fetch:
        for remote in remotes:
            fetch(remote)

    result = {}
    for rb in branches('-r'):
        remote, branch = rb.split('/')
        result.setdefault(remote, []).append(branch)
    return result


def force_flags():
    return ['--force-with-lease'] if PROGRAM.args.force else []
