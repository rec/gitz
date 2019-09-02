from . import git_functions
import json
import os

PREFIX = 'GITZ_'
CONFIG_FILE = '.gitz.json'


class Env:
    DEFAULTS = {
        'PROTECTED_BRANCHES': 'develop:master:release',
        'PROTECTED_REMOTES': 'upstream',
        'REFERENCE_BRANCHES': 'develop:master',
        'ORIGIN': 'origin',
        'UPSTREAM': 'upstream:origin',
    }

    def __getattr__(self, key):
        return lambda: self.get(key)

    def get(self, key):
        key = key.upper()
        default = self.DEFAULTS.get(key)
        if default is None:
            raise KeyError(key)

        value = os.environ.get(PREFIX + key)
        if value is not None:
            return value

        root = git_functions.find_git_root()
        value = None
        if root and (root / CONFIG_FILE).exists():
            config = json.load(open(str(root / CONFIG_FILE)))
            value = config.get(key, config.get(key.lower()))

        if value is None:
            value = default
        return value.split(':')


ENV = Env()
