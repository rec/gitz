from . import repo
from gitz.git import functions
from gitz.git import GIT
import unittest


class GitStripeTest(unittest.TestCase):
    @repo.test
    def test_stripe(self):
        self._setup()
        GIT.stripe('-d', '-v')
        actual = functions.branches('-r')
        expected = ['origin/master', 'upstream/master']
        self.assertEqual(actual, expected)

    @repo.test
    def test_error(self):
        self._setup()
        with self.assertRaises(ValueError):
            GIT.stripe('-d', 'foo', '-v')
        with self.assertRaises(ValueError):
            GIT.stripe('-d', '-c2', '-v')

    @repo.test
    def test_range_setting(self):
        repo.make_commit('1')
        two = repo.make_commit('2')
        repo.make_commit('3')
        four = repo.make_commit('4')
        repo.make_commit('5')

        GIT.push('-u', 'origin', 'master')
        GIT.stripe(two, four, '-v')

        actual = functions.branches('-r')
        expected = [
            'origin/_gitz_stripe_0',
            'origin/_gitz_stripe_1',
            'origin/master',
            'upstream/master',
        ]
        self.assertEqual(actual, expected)

    @repo.test
    def test_offset(self):
        repo.make_commit('1')
        repo.make_commit('2')
        GIT.push('-u', 'origin', 'master')
        GIT.stripe('-v', '-o3', '-c2')
        actual = functions.branches('-r')
        expected = [
            'origin/_gitz_stripe_3',
            'origin/_gitz_stripe_4',
            'origin/master',
            'upstream/master',
        ]
        self.assertEqual(actual, expected)
        GIT.stripe('-vd')
        expected = ['origin/master', 'upstream/master']

    def _setup(self):
        repo.make_commit('1')
        repo.make_commit('2')
        repo.make_commit('3')
        repo.make_commit('4')

        GIT.push('-u', 'origin', 'master')
        GIT.stripe('-c3', '-v')

        actual = functions.branches('-r')
        expected = [
            'origin/_gitz_stripe_0',
            'origin/_gitz_stripe_1',
            'origin/_gitz_stripe_2',
            'origin/master',
            'upstream/master',
        ]
        self.assertEqual(actual, expected)
