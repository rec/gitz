import unittest
from . import repo
from _gitz import GIT


class RepoTest(unittest.TestCase):
    @repo.method
    def test_repo(self):
        self.assertEqual('047f436', repo.make_commit('one.txt'))
        with self.assertRaises(Exception):
            repo.make_commit('one.txt')

        self.assertEqual('33bb2c0', repo.make_commit('two.txt'))

    @repo.method
    def test_clones(self):
        self.assertEqual('047f436', repo.make_commit('one.txt'))
        self.assertEqual('33bb2c0', repo.make_commit('two.txt'))
        GIT.checkout('-b', 'working')

        with repo.clones('foo', 'bar'):
            self.assertEqual(sorted(GIT.remote()), ['bar', 'foo'])
            GIT.fetch('foo')
            GIT.fetch('bar')
            actual = GIT.branches('-r')
            expected = [
                'bar/master',
                'bar/working',
                'foo/master',
                'foo/working',
            ]
            self.assertEqual(actual, expected)
            self.assertEqual('435d066', repo.make_commit('three.txt'))
            GIT.push('foo', 'HEAD:working')
            self.assertEqual(GIT.commit_id('bar/working'), '33bb2c0')
            self.assertEqual(GIT.commit_id('foo/working'), '435d066')
