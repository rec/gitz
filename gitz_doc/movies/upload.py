from .constants import ALL_COMMANDS_CAST
from .constants import ALL_COMMANDS_JSON
from gitz.program import run_proc
import hashlib
import json


def all_movie_url():
    m = hashlib.sha256()
    m.update(ALL_COMMANDS_CAST.read_bytes())
    sha = m.hexdigest()

    if ALL_COMMANDS_JSON.exists():
        new_sha, url = json.loads(ALL_COMMANDS_JSON.read_text())
        if new_sha == sha:
            return url

    lines = run_proc.run_proc(COMMAND)
    url = next(i for i in lines if 'https://' in i).strip()
    ALL_COMMANDS_JSON.write_text(json.dumps([sha, url]))
    print(MESSAGE.format(url=url))


COMMAND = 'asciinema', 'upload', str(ALL_COMMANDS_CAST)
MESSAGE = """
New upload created!

Now you need to make the upload public and change its name to
"The gitz movie".  Go to:

   {url}
"""
