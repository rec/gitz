from . import repo
from gitz.program import git
from gitz.program import safe_git
import os
import unittest


class GitMultiPickTest(unittest.TestCase):
    @repo.test
    def test_simple(self):
        self._get_files()
        expected = ['a023846 5', '2511fd4 3', 'c0d1dbb 0']
        self.assertEqual(safe_git.log('--oneline'), expected)

    @repo.test
    def test_squash(self):
        self._get_files('-s="0 3 5"')
        expected = ['ad627aa "0 3 5"', 'c0d1dbb 0']
        self.assertEqual(safe_git.log('--oneline'), expected)

    def _get_files(self, *args):
        git.checkout('-b', 'A')
        repo.make_commit('1')
        repo.make_commit('2')
        three = repo.make_commit('3')
        repo.make_commit('4')
        five = repo.make_commit('5')
        repo.make_commit('6')

        git.checkout('master')
        git('multi-pick', three, five, *args)
        files = sorted(i for i in os.listdir() if not i.startswith('.'))
        self.assertEqual(files, ['0', '3', '5'])
