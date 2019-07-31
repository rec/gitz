from . import repo
from gitz import runner
import unittest


class RunnerTest(unittest.TestCase):
    @repo.test
    def test_simple(self):
        logger = MockLogger()
        git = runner.GitRunners(logger, MockLogger())
        returncode, stdout = git.run('ls')
        self.assertEqual(returncode, 0)
        self.assertEqual(stdout, ['0\n'])
        self.assertEqual(logger.commands, [('ls',)])
        self.assertEqual(logger.stdouts, ['0\n'])
        self.assertEqual(logger.stderrs, [])
        with open('X', 'w') as fp:
            fp.write('X\n')
        git.add('X')


class MockLogger:
    def __init__(self):
        self.commands = []
        self.stdouts = []
        self.stderrs = []

    def command(self, *cmd):
        self.commands.append(cmd)

    def stdout(self, line):
        self.stdouts.append(line)

    def stderr(self, line):
        self.stderrs.append(line)
