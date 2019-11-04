import contextlib
from pathlib import Path

SUFFIX = '.tmp'


@contextlib.contextmanager
def safe_writer(filename, suffix=SUFFIX, create_parents=True):
    tempfile = Path(str(filename) + suffix)
    if create_parents:
        tempfile.parent.mkdir(parents=True, exist_ok=True)
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
