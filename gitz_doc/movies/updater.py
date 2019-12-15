from .cast import Cast
from . import render
from gitz.program import safe_writer
from pathlib import Path

ROOT = Path(__file__).parent


class Updater:
    @staticmethod
    def render(cast, cast_file, target):
        cast.write(cast_file)
        render.render(cast, target)

    @classmethod
    def update(cls, commands):
        all_casts = Cast()
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
            all_casts.update(cast)
            print(symbol, up.target)

        cls.render(all_casts, cls.ALL_CASTS, cls.ALL_SVG)
        print('wrote', cls.ALL_SVG)
