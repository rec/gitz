from pathlib import Path

ROOT = Path(__file__).parent


class Updater:
    @classmethod
    def update(cls, commands):
        results = []
        for c in commands:
            symbol, result = cls._update(cls._target(c), cls._source(c))
            if result:
                results.append((c, result))

        return results

    @classmethod
    def _update(cls, target, source):
        if not source.exists():
            return '?', None

        new = cls._needs_update(target, source)
        symbol = '+' if new else '.'
        method = cls._create if new else cls._existing
        return symbol, method(target, source)

    @classmethod
    def _needs_update(cls, target, source):
        if not target.exists():
            return True
        src = tuple(f for f in ROOT.iterdir() if f.suffix == '.py')
        newest = max(f.stat().st_mtime for f in src + (source,))
        return target.stat().st_mtime < newest
