from pathlib import Path

ROOT = Path(__file__).parent
LAST_MODIFIED = max(f.stat().st_mtime for f in Path(__file__).parent.iterdir())


def needs_update(target, *dependencies):
    if not all(f.exists() for f in dependencies):
        return '?'
    if not target.exists():
        return '+'

    src = tuple(f for f in ROOT.iterdir() if f.suffix == '.py')
    newest = max(f.stat().st_mtime for f in src + dependencies)
    return '+' if target.stat().st_mtime < newest else '.'
