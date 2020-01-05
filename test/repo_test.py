from . import repo
from gitz.git import functions
from gitz.git import GIT
import unittest


class RepoTest(unittest.TestCase):
    @repo.test
    def test_repo(self):
        self.assertEqual('44dac6b', repo.make_commit('one.txt'))
        with self.assertRaises(Exception):
            repo.make_commit('one.txt')

        self.assertEqual('393ad1c', repo.make_commit('two.txt'))

    @repo.test
    def test_clone(self):
        self.assertEqual('44dac6b', repo.make_commit('one.txt'))
        self.assertEqual('393ad1c', repo.make_commit('two.txt'))
        GIT.checkout('-b', 'working')

        repo.add_remotes(['foo', 'bar'])
        expected = ['bar', 'foo', 'origin', 'upstream']
        self.assertEqual(sorted(GIT.remote()), expected)
        functions.fetch('foo')
        functions.fetch('bar')
        actual = functions.branches('-r')
        expected = [
            'bar/working',
            'foo/working',
            'origin/master',
            'upstream/master',
        ]
        self.assertEqual(actual, expected)
        self.assertEqual('efc4ce6', repo.make_commit('three.txt'))
        GIT.push('foo', 'HEAD:working')
        self.assertEqual(functions.commit_id('bar/working'), '393ad1c')
        self.assertEqual(functions.commit_id('foo/working'), 'efc4ce6')
