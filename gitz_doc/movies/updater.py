from gitz.program import safe_writer
from pathlib import Path

ROOT = Path(__file__).parent


class Updater:
    @classmethod
    def update(cls, commands):
        results = []
        for command in commands:
            up = cls(command)
            if not up.source.exists():
                print('?', up.target)
                continue

            if not up.target.exists():
                new = True
            else:
                src = tuple(f for f in ROOT.iterdir() if f.suffix == '.py')
                newest = max(f.stat().st_mtime for f in src + (up.source,))
                new = up.target.stat().st_mtime < newest

            if new:
                symbol = '+'
                safe_writer.make_parents(up.target)
                cast = up._create()
            else:
                symbol = '.'
                cast = up._existing()

            print(symbol, up.target)
            results.append((symbol, cast))

        return results
