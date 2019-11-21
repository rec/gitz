from . import functions


def commit_range(c1, c2):
    def is_number(x):
        return x.isnumeric() and len(x) < 7

    if not c2:
        commit_id, count = c1, c2
    elif not is_number(c1):
        commit_id, count = c1, c2
    elif not is_number(c2):
        commit_id, count = c2, c1
    else:
        raise ValueError('Only one of count and commit id can be a number')

    commit_id = commit_id or 'HEAD~'
    cid = functions.commit_id(commit_id)
    count = count or '1'

    if is_number(count):
        return cid, int(count)

    count_id = functions.commit_id(count)
    if functions.is_ancestor(count_id, cid):
        parent, child = count_id, cid
    elif functions.is_ancestor(cid, count_id):
        parent, child = cid, count_id
    else:
        raise ValueError('%s, %s not in the same history' % (count, commit_id))

    count = 1
    node = child
    while node != parent:
        count += 1
        node = functions.commit_id(node + '~')

    return child, count
