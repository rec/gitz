from gitz.git import GIT
from gitz.git import functions
from gitz.git import repo
import unittest


class GitDeleteTest(unittest.TestCase):
    @repo.test
    def test_delete(self):
        GIT.new('one')
        repo.make_commit('1')
        GIT.push()

        GIT.new('two')
        repo.make_commit('2')
        GIT.push()

        actual = functions.branches('-r')
        expected = [
            'origin/master',
            'origin/one',
            'origin/two',
            'upstream/master',
        ]
        self.assertEqual(actual, expected)

        GIT.delete('one', 'two', '-v')
        actual = functions.branches('-r')
        expected = ['origin/master', 'upstream/master']
        self.assertEqual(actual, expected)
