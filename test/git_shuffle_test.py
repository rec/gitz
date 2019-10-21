from . import repo
from gitz.runner import GIT
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
        GIT.shuffle('__cba_')
        actual = GIT.log('--oneline')[:4]
        expected = []
        self.assertEqual(actual, expected)

    @repo.test
    def test_reverse(self):
        self._first()
        GIT.shuffle('ba')
        actual = GIT.log('--oneline')[:4]
        expected = ['85af3d4 6', 'd9b4446 7', '8a4a4e2 5', 'a7c7e8f 4']
        self.assertEqual(actual, expected)

    @repo.test
    def test_squash(self):
        self._test_files('-s="0 1 3 4 6"')
        actual = GIT.log('--oneline')
        expected = ['a60e28d "0 1 3 4 6"', 'a03c0f8 1', 'c0d1dbb 0']
        self.assertEqual(actual, expected)

    @repo.test
    def test_empty_squash(self):
        self._test_files('-s')
        actual = GIT.log('--oneline')
        expected = ['dc12af1 4', 'a03c0f8 1', 'c0d1dbb 0']
        self.assertEqual(actual, expected)

    def _first(self):
        repo.make_commit('1')
        repo.make_commit('2')
        repo.make_commit('3')
        repo.make_commit('4')
        repo.make_commit('5')
        repo.make_commit('6')
        repo.make_commit('7')

        actual = GIT.log('--oneline')
        expected = [
            'e487041 7',
            'e1e931a 6',
            '8a4a4e2 5',
            'a7c7e8f 4',
            '9ab30c5 3',
            '043df1f 2',
            'a03c0f8 1',
            'c0d1dbb 0',
        ]
        self.assertEqual(actual, expected)

    def _test_files(self, *args):
        self._first()
        GIT.shuffle('_c_ab_', *args)
        files = [i for i in os.listdir() if not i.startswith('.')]
        self.assertEqual(sorted(files), ['0', '1', '3', '4', '6'])
