from gitz import config
from gitz.git import GIT
from gitz.git import repo
from gitz.program import summaries
from pathlib import Path
import platform
import unittest


class GitGitzTest(unittest.TestCase):
    maxDiff = 100000

    @repo.test
    def test_all(self):
        # See #170
        indent_commands = (('    ' if c else '') + c for c in COMMANDS)
        indent_commands = '\n'.join(indent_commands)
        home_page = config.HOME_PAGE
        executable_directory = str(config.EXECUTABLE_DIRECTORY)
        library_directory = str(config.LIBRARY_DIRECTORY)
        version = config.VERSION
        python_version = platform.python_version()
        platform_name = platform.platform()
        commands = list(_commands())
        indent_commands = indent_commands

        def filter_results(lines):
            results = []
            prev = ''
            py = '    Python'
            xd = 'Executable directory:'
            for line in lines:
                if not (line.startswith(py) or prev.startswith(xd)):
                    results.append(line)
                prev = line
            return results

        results = RESULTS.format(**locals())
        expected = filter_results(results.splitlines())
        actual = filter_results(GIT.gitz('-v'))
        self.assertEqual(expected, actual)

    @repo.test
    def test_version(self):
        for v in 'v', 've', 'version':
            self.assertEqual(GIT.gitz(v, '-v'), [config.VERSION])

    @repo.test
    def test_commands(self):
        expected = COMMANDS
        for c in 'c', 'com', 'commands':
            actual = GIT.gitz(c, '-v')
            self.assertEqual(actual, expected)
            self.assertEqual(len(actual), len(expected))

    @repo.test
    def test_executable_directory(self):
        result = {
            GIT.gitz(d, '-v')[0] for d in ('e', 'exec', 'executable_directory')
        }
        self.assertEqual(len(result), 1)
        result = next(iter(result))
        self.assertTrue((Path(result) / 'git-gitz').exists())

    @repo.test
    def test_library_directory(self):
        for d in 'l', 'libr', 'library_directory':
            self.assertEqual(
                GIT.gitz(d, '-v'), [str(config.LIBRARY_DIRECTORY)]
            )

    @repo.test
    def test_defaults(self):
        for d in 'd', 'def', 'defaults':
            self.assertEqual(GIT.gitz(d, '-v'), DEFAULTS)

    @repo.test
    def test_error(self):
        with self.assertRaises(ValueError):
            GIT.gitz('var', '-v')

        with self.assertRaises(ValueError):
            GIT.gitz('Com', '-v')


def _commands():
    for i, (cmd, summary) in enumerate(sorted(summaries.SUMMARIES.items())):
        if i and not (i % 4):
            yield ''

        yield cmd + ':'
        yield '    ' + summary


COMMANDS = list(_commands())

RESULTS = """\
Commands:
{indent_commands}

Defaults:
    GITZ_ORIGIN = ['origin']
    GITZ_PROTECTED_BRANCHES = ['develop', 'master', 'release']
    GITZ_REFERENCE_BRANCHES = ['develop', 'master']
    GITZ_UPSTREAM = ['upstream', 'origin']

Executable directory:
    {executable_directory}

Home page:
    {home_page}

Library directory:
    {library_directory}

Python:
    Python v{python_version} on {platform_name}

Version:
    {version}
"""

DEFAULTS = """\
GITZ_ORIGIN = ['origin']
GITZ_PROTECTED_BRANCHES = ['develop', 'master', 'release']
GITZ_REFERENCE_BRANCHES = ['develop', 'master']
GITZ_UPSTREAM = ['upstream', 'origin']
""".splitlines()
