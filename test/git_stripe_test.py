from . import repo
from gitz.git import functions
from gitz.git import GIT
import unittest


class GitStripeTest(unittest.TestCase):
    @repo.test
    def test_stripe(self):
        repo.make_commit('1')
        repo.make_commit('2')
        repo.make_commit('3')
        repo.make_commit('4')

        GIT.push('-u', 'origin', 'master')
        GIT.stripe('3', '-v')

        actual = functions.branches('-r')
        expected = [
            'origin/_gitz_stripe_0',
            'origin/_gitz_stripe_1',
            'origin/_gitz_stripe_2',
            'origin/master',
            'upstream/master',
        ]
        self.assertEqual(actual, expected)

        GIT.stripe('3', '-d', '-v')
        actual = functions.branches('-r')
        expected = ['origin/master', 'upstream/master']
        self.assertEqual(actual, expected)

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
            'origin/_gitz_stripe_2',
            'origin/master',
            'upstream/master',
        ]
        self.assertEqual(actual, expected)
