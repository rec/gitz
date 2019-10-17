from . import repo
from gitz import git_functions
from gitz.program import PROGRAM
from gitz.runner import GIT_INFO
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
        PROGRAM.git.checkout('-b', 'working')

        with repo.clone('foo', 'bar'):
            expected = ['bar', 'foo', 'origin', 'upstream']
            self.assertEqual(sorted(GIT_INFO.remote()), expected)
            git_functions.fetch('foo')
            git_functions.fetch('bar')
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
            PROGRAM.git.push('foo', 'HEAD:working')
            self.assertEqual(git_functions.commit_id('bar/working'), '393ad1c')
            self.assertEqual(git_functions.commit_id('foo/working'), 'efc4ce6')
