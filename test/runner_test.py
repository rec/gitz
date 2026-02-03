import unittest

from gitz.git import repo
from gitz.program import runner


class RunnerTest(unittest.TestCase):
    @repo.test
    def test_simple(self):
        logger = MockLogger()
        run = runner.Runner()
        run.start(logger)
        stdout = run('ls')
        self.assertEqual(stdout, ['0'])
        self.assertEqual(logger.errors, [])
        self.assertEqual(logger.messages, [])
        self.assertEqual(logger.verboses, [('$', 'ls'), ('>', '0')])
        with open('X', 'w') as fp:
            fp.write('X\n')
        git = runner.Git(run)
        git.add('X')

    @repo.test
    def test_multiline(self):
        logger = MockLogger()
        run = runner.Runner()
        run.start(logger)
        with open('X', 'w') as fp:
            fp.write('X\n')
        stdout = run('ls')
        self.assertEqual(stdout, ['0', 'X'])


class MockLogger:
    def __init__(self):
        self.verboses = []
        self.messages = []
        self.errors = []

    def error(self, *parts):
        self.errors.append(parts)

    def message(self, *parts):
        self.messages.append(parts)

    def verbose(self, *parts):
        self.verboses.append(parts)
