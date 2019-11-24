from gitz import config
from pathlib import Path

GITZ_ROOT = Path(__file__).parent.parent


def commands():
    print('SUMMARIES = {')
    for command in config.COMMANDS:
        summary = SUMMARIES.get(command)
        if not summary:
            file = GITZ_ROOT / command
            source = file.read_text()
            compiled = compile(source, str(file), 'exec')
            context = {}
            exec(compiled, context)
            summary = context['SUMMARY']

        print("    '%s': '%s'," % (command, summary))
    print('}')


SUMMARIES = {
    'git-amp': 'AMend the last commit message and force-Push, somewhat safely',
    'git-infer': 'Commit changes with an auto-generated message',
    'git-st': 'Colorful, compact git status',
    'git-when': 'When did each file change (date, commit, message)?',
}


if __name__ == '__main__':
    commands()
