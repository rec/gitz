import json
import os

PREFIX = 'GITZ_'
CONFIG_FILE = '.gitz.json'


class Env:
    DEFAULTS = {
        'PROTECTED_BRANCHES': 'develop:main:master',
        'REFERENCE_BRANCHES': 'develop:main:master',
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

        from ..git import root

        groot = root.root()
        value = None
        if groot and (groot / CONFIG_FILE).exists():
            config = json.load(open(str(groot / CONFIG_FILE)))
            value = config.get(key, config.get(key.lower()))

        if value is None:
            value = default
        return value.split(':')


ENV = Env()
