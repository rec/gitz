import contextlib
from pathlib import Path

SUFFIX = '.tmp'


def make_parents(file):
    file.parent.mkdir(parents=True, exist_ok=True)


@contextlib.contextmanager
def safe_writer(filename, suffix=SUFFIX, create_parents=True, overwrite=True):
    path = Path(filename)
    if not overwrite and path.exists():
        raise ValueError('Cannot overwrite ' + str(path))

    tempfile = Path(str(filename) + suffix)
    if tempfile.exists():
        raise ValueError('Tempfile %s exists!' % str(tempfile))

    if create_parents:
        make_parents(tempfile)

    with tempfile.open('w') as fp:
        try:
            yield fp
        except Exception:
            try:
                tempfile.unlink()
            except Exception:
                pass
            raise

    tempfile.rename(filename)
