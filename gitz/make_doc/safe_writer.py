import contextlib
import os
SUFFIX = '.tmp'


@contextlib.contextmanager
def safe_writer(filename, suffix=SUFFIX):
    tempfile = filename + suffix
    with open(tempfile, 'w') as fp:
        try:
            yield fp
        except Exception:
            try:
                os.remove(tempfile)
            except Exception:
                pass
            raise

    os.rename(tempfile, filename)
