from . import repo
from gitz import git_functions
from gitz.program import git
from gitz.program import safe_git
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
        git.checkout('-b', 'working')

        with repo.clone('foo', 'bar'):
            expected = ['bar', 'foo', 'origin', 'upstream']
            self.assertEqual(sorted(safe_git.remote()), expected)
            git.fetch('foo')
            git.fetch('bar')
            actual = git_functions.branches('-r')
            expected = [
                'bar/master',
                'bar/working',
                'foo/master',
                'foo/working',
                'origin/master',
                'upstream/master',
            ]
            self.assertEqual(actual, expected)
            self.assertEqual('efc4ce6', repo.make_commit('three.txt'))
            git.push('foo', 'HEAD:working')
            self.assertEqual(
                git_functions.commit_id('bar/working'),
                '393ad1c265321cdf4d25661379a1fd6922933c40',
            )
            self.assertEqual(
                git_functions.commit_id('foo/working'),
                'efc4ce65521dbd7a2f410bcc782a088c4460afc5',
            )
