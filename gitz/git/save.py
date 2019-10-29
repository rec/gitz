from . import GIT
from . import functions
from . import root
import datetime
import os

NONE, STAGED, CHANGED, UNTRACKED = 'none', 'staged', 'changed', 'untracked'
PREFIX = '_gitz_'


def save(untracked=False):
    timestamp = datetime.datetime.now().strftime('%c')

    def commit(flag, name):
        try:
            GIT.commit(flag, '%s%s: %s' % (PREFIX, name, timestamp))
        except Exception:
            pass

    commit('-m', STAGED)
    commit('-am', CHANGED)

    if untracked:
        saved = os.getcwd()
        root.cd_root()

        GIT.add('.')
        commit('-m', UNTRACKED)

        os.chdir(saved)

    state = functions.commit_id()
    restore(state)
    return state


def restore(state):
    GIT.reset('--hard', state)
    msg = functions.message('HEAD')

    while msg.startswith(PREFIX):
        msg = functions.message('HEAD~')
        if msg.startswith(PREFIX):
            GIT.reset('--mixed', 'HEAD~')
        else:
            GIT.reset('--soft', 'HEAD~')
