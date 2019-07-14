import unittest
import _gitz
from . import repo

GIT = _gitz.GIT


class RepoTest(unittest.TestCase):
    @repo.method
    def test_repo(self):
        self.assertEqual('44dac6b', repo.make_commit('one.txt'))
        with self.assertRaises(Exception):
            repo.make_commit('one.txt')

        self.assertEqual('393ad1c', repo.make_commit('two.txt'))

    @repo.method
    def test_clone(self):
        self.assertEqual('44dac6b', repo.make_commit('one.txt'))
        self.assertEqual('393ad1c', repo.make_commit('two.txt'))
        GIT.checkout('-b', 'working')

        with repo.clone('foo', 'bar'):
            expected = ['bar', 'foo', 'origin', 'upstream']
            self.assertEqual(sorted(GIT.remote()), expected)
            GIT.fetch('foo')
            GIT.fetch('bar')
            actual = _gitz.branches('-r')
            expected = [
                'bar/master',
                'bar/working',
                'foo/master',
                'foo/working',
            ]
            self.assertEqual(actual, expected)
            self.assertEqual('efc4ce6', repo.make_commit('three.txt'))
            GIT.push('foo', 'HEAD:working')
            self.assertEqual(_gitz.commit_id('bar/working'), '393ad1c')
            self.assertEqual(_gitz.commit_id('foo/working'), 'efc4ce6')
