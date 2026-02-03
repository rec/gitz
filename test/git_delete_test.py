import unittest

from gitz.git import GIT, functions, repo


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
            'origin/main',
            'origin/one',
            'origin/two',
            'upstream/main',
        ]
        self.assertEqual(actual, expected)

        GIT.delete('one', 'two', '-v')
        actual = functions.branches('-r')
        expected = ['origin/main', 'upstream/main']
        self.assertEqual(actual, expected)
