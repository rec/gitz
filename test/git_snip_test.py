from . import repo
import os
import unittest
GIT = repo.GIT


class GitSnipTest(unittest.TestCase):
    @repo.method
    def test_simple(self):
        repo.make_commit('0')
        one = repo.make_commit('1')
        repo.make_commit('2')
        three = repo.make_commit('3')
        repo.make_commit('4')
        repo.make_commit('5')
        repo.make_commit('6')

        GIT.git('snip', one, three, 'HEAD~')
        files = [i for i in os.listdir() if not i.startswith('.')]
        self.assertEqual(files, ['0', '2', '4', '6'])
