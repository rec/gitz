from . import repo
from gitz.program import git
import os
import unittest


def _get_files(*args):
    one = repo.make_commit('1')
    repo.make_commit('2')
    three = repo.make_commit('3')
    repo.make_commit('4')
    repo.make_commit('5')
    repo.make_commit('6')

    git.combine('-b=%s~' % one, three, 'HEAD~', *args)
    return [i for i in os.listdir() if not i.startswith('.')]


class GitCombineTest(unittest.TestCase):
    @repo.test
    def test_simple(self):
        files = _get_files()
        self.assertEqual(sorted(files), ['0', '3', '5'])
        expected = ['a023846 5', '2511fd4 3', 'c0d1dbb 0']
        self.assertEqual(git.log('--oneline'), expected)

    @repo.test
    def test_squash(self):
        files = _get_files('-s="0 3 5"')
        self.assertEqual(sorted(files), ['0', '3', '5'])
        expected = ['ad627aa "0 3 5"', 'c0d1dbb 0']
        self.assertEqual(git.log('--oneline'), expected)
