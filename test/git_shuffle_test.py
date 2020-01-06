from . import repo
from gitz.git import GIT
import os
import unittest


class GitShuffleTest(unittest.TestCase):
    @repo.test
    def test_test_files(self):
        self._test_files()
        actual = GIT.log('--oneline')
        expected = [
            '2a2c087 3',
            '4fbc0b7 6',
            'adf954d 4',
            'a03c0f8 1',
            'c0d1dbb 0',
        ]
        self.assertEqual(actual, expected)

    @repo.test
    def TODO_test_example(self):
        # Why does this fail?  Debugging gives nonsensical results!
        # GIT.shuffle('__cba_', '-v')
        GIT.shuffle('edcf', '-v')
        actual = GIT.log('--oneline')[:4]
        expected = []
        self.assertEqual(actual, expected)

    @repo.test
    def test_reverse(self):
        repo.make_seven_commits(self)
        GIT.shuffle('ba', '-v')
        actual = GIT.log('--oneline')[:4]
        expected = ['85af3d4 6', 'd9b4446 7', '8a4a4e2 5', 'a7c7e8f 4']
        self.assertEqual(actual, expected)

    @repo.test
    def test(self):
        repo.make_seven_commits(self)
        GIT.shuffle('01234', '-v', '-s', 'TEST')

        actual = GIT.log('--oneline')
        expected = ['bbd9e40 TEST', '043df1f 2', 'a03c0f8 1', 'c0d1dbb 0']
        self.assertEqual(actual, expected)

    @repo.test
    def test_empty_squash(self):
        repo.make_seven_commits(self)
        GIT.shuffle('01234', '-v', '-s')

        actual = GIT.log('--oneline')
        expected = ['059f1ee 3', '043df1f 2', 'a03c0f8 1', 'c0d1dbb 0']
        self.assertEqual(actual, expected)

    def _test_files(self):
        repo.make_seven_commits(self)
        GIT.shuffle('ebdg', '-v')
        files = [i for i in os.listdir() if not i.startswith('.')]
        self.assertEqual(sorted(files), ['0', '1', '3', '4', '6'])
