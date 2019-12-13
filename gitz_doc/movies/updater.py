from gitz.program import safe_writer
from pathlib import Path

ROOT = Path(__file__).parent


class Updater:
    # These need to be overridden in the derived class
    _target = _source = _create = _existing = None

    @classmethod
    def update(cls, commands):
        results = []
        for command in commands:
            target = cls._target(command)
            source = cls._source(command)
            if not source.exists():
                print('?', target)
                continue

            if not target.exists():
                new = True
            else:
                src = tuple(f for f in ROOT.iterdir() if f.suffix == '.py')
                newest = max(f.stat().st_mtime for f in src + (source,))
                new = target.stat().st_mtime < newest

            if new:
                symbol = '+'
                safe_writer.make_parents(target)
                cast = cls._create(command, target)
            else:
                symbol = '.'
                cast = cls._existing(command, target)

            print(symbol, target)
            results.append((symbol, cast))

        return results
