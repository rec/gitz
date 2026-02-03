import unittest

from gitz.git import GIT, functions, repo


def stripe(*parts):
    GIT.stripe('-v', *' '.join(parts).split())


class GitStripeTest(unittest.TestCase):
    @repo.test
    def test_stripe(self):
        self._setup()
        stripe('--delete')
        actual = functions.branches('-r')
        expected = ['origin/main', 'upstream/main']
        self.assertEqual(actual, expected)

    @repo.test
    def test_error(self):
        self._setup()
        with self.assertRaises(ValueError):
            stripe('--delete foo')
        with self.assertRaises(ValueError):
            stripe('--delete --count=2')

    @repo.test
    def test_range_setting(self):
        repo.make_commit('1')
        two = repo.make_commit('2')
        repo.make_commit('3')
        four = repo.make_commit('4')
        repo.make_commit('5')

        GIT.push('-u', 'origin', 'main')
        stripe(two, four)

        actual = functions.branches('-r')
        expected = [
            'origin/_gitz_stripe_0',
            'origin/_gitz_stripe_1',
            'origin/main',
            'upstream/main',
        ]
        self.assertEqual(actual, expected)

    @repo.test
    def test_offset_and_safe(self):
        repo.make_commit('1')
        repo.make_commit('2')
        GIT.push('-u', 'origin', 'main')
        stripe('--count=2 --offset=3')
        actual = functions.branches('-r')
        expected = [
            'origin/_gitz_stripe_3',
            'origin/_gitz_stripe_4',
            'origin/main',
            'upstream/main',
        ]
        self.assertEqual(actual, expected)

        stripe('--count=2 --safe')
        actual = functions.branches('-r')
        expected = [
            'origin/_gitz_stripe_3',
            'origin/_gitz_stripe_4',
            'origin/_gitz_stripe_5',
            'origin/_gitz_stripe_6',
            'origin/main',
            'upstream/main',
        ]
        self.assertEqual(actual, expected)

    def _setup(self):
        repo.make_commit('1')
        repo.make_commit('2')
        repo.make_commit('3')
        repo.make_commit('4')

        GIT.push('-u', 'origin', 'main')
        stripe('--count=3')

        actual = functions.branches('-r')
        expected = [
            'origin/_gitz_stripe_0',
            'origin/_gitz_stripe_1',
            'origin/_gitz_stripe_2',
            'origin/main',
            'upstream/main',
        ]
        self.assertEqual(actual, expected)
