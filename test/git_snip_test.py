from . import repo
from gitz.program import dry_git
import os
import unittest


class GitSnipTest(unittest.TestCase):
    @repo.test
    def test_simple(self):
        one = repo.make_commit('1')
        repo.make_commit('2')
        three = repo.make_commit('3')
        repo.make_commit('4')
        repo.make_commit('5')
        repo.make_commit('6')

        dry_git.snip(one, three, 'HEAD~')
        files = [i for i in os.listdir() if not i.startswith('.')]
        self.assertEqual(sorted(files), ['0', '2', '4', '6'])
