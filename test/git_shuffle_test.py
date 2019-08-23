from . import repo
from gitz.program import git
import os
import unittest


class GitShuffleTest(unittest.TestCase):
    @repo.test
    def test_simple(self):
        self._get_files()
        actual = git.log('--oneline')
        expected = [
            '2a2c087 3',
            '4fbc0b7 6',
            'adf954d 4',
            'a03c0f8 1',
            'c0d1dbb 0',
        ]
        self.assertEqual(actual, expected)

    @repo.test
    def test_squash(self):
        self._get_files('-s="0 1 3 4 6"')
        actual = git.log('--oneline')
        expected = ['a60e28d "0 1 3 4 6"', 'a03c0f8 1', 'c0d1dbb 0']
        self.assertEqual(actual, expected)

    def _get_files(self, *args):
        repo.make_commit('1')
        repo.make_commit('2')
        repo.make_commit('3')
        repo.make_commit('4')
        repo.make_commit('5')
        repo.make_commit('6')
        repo.make_commit('7')

        actual = git.log('--oneline')
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
        git.shuffle('_c_ab_', *args)
        files = [i for i in os.listdir() if not i.startswith('.')]
        self.assertEqual(sorted(files), ['0', '1', '3', '4', '6'])
