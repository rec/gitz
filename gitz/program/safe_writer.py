import contextlib
from pathlib import Path

SUFFIX = '.tmp'


def make_parents(file):
    file.parent.mkdir(parents=True, exist_ok=True)


@contextlib.contextmanager
def safe_writer(filename, suffix=SUFFIX, create_parents=True):
    tempfile = Path(str(filename) + suffix)
    if create_parents:
        make_parents(tempfile)

    with tempfile.open('w') as fp:
        try:
            yield fp
        except Exception:
            try:
                tempfile.remove()
            except Exception:
                pass
            raise

    tempfile.rename(filename)
