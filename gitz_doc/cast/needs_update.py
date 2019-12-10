from pathlib import Path

ROOT = Path(__file__).parent


class Updater:
    # These need to be overridden in the derived class
    _target = _source = _create = _existing = None

    @classmethod
    def update(cls, commands):
        results = []
        for c in commands:
            target = cls._target(c)
            source = cls._source(c)
            if not source.exists():
                print('?', target)
                continue

            if target.exists():
                new = True
            else:
                src = tuple(f for f in ROOT.iterdir() if f.suffix == '.py')
                newest = max(f.stat().st_mtime for f in src + (source,))
                new = target.stat().st_mtime < newest

            if new:
                symbol = '+'
                cast = cls._create(target, source)
            else:
                symbol = '.'
                cast = cls._existing(target, source)

            results.append((symbol, cast))

        return results
