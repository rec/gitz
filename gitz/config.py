from pathlib import Path

VERSION = '0.9.11'
ROOT_DIR = Path(__file__).absolute().parents[1]
COMMANDS = sorted(
    f.name for f in ROOT_DIR.iterdir() if f.name.startswith('git-')
)
README = ROOT_DIR / 'README.rst'
