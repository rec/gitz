from . import GIT
from . import functions
from . import root
from pathlib import Path
import datetime
import os

NONE, STAGED, CHANGED, UNTRACKED = 'none', 'staged', 'changed', 'untracked'
PREFIX = '_gitz_'
SAVE_FILE = Path('._gitz_save_.txt')


@root.run_in_root
def save(untracked=False, stash=True):
    timestamp = datetime.datetime.now().strftime('%c')

    def commit(flag, name):
        try:
            GIT.commit(flag, '%s%s: %s' % (PREFIX, name, timestamp))
        except Exception:
            pass

    commit('-m', STAGED)
    commit('-am', CHANGED)

    if untracked:
        GIT.add('.')
        commit('-m', UNTRACKED)

    state = functions.commit_id()
    if stash:
        SAVE_FILE.write_text(state)
        GIT.add(SAVE_FILE)
        GIT.stash()

    restore(state)
    return state


def restore(state):
    if state == 'pop':
        GIT.stash('pop')
        if not SAVE_FILE.exists():
            GIT.stash()
            raise ValueError('Stash was not built with gitz-save')

        state = SAVE_FILE.read_text().strip()
        os.remove(str(SAVE_FILE))

    GIT.reset('--hard', state)
    GIT.clean('-f')
    msg = functions.message('HEAD')

    while msg.startswith(PREFIX):
        msg = functions.message('HEAD~')
        if msg.startswith(PREFIX):
            GIT.reset('--mixed', 'HEAD~')
        else:
            GIT.reset('--soft', 'HEAD~')
