from . import repo
from gitz.runner import GIT
import unittest


class GitAmpTest(unittest.TestCase):
    @repo.test
    def test_simple(self):
        repo.make_commit('1')
        GIT.checkout('-b', 'develop', info=True)

        GIT.push('--set-upstream', 'origin', 'develop', info=True)
        GIT.amp('Hello', 'there', 'mates', info=True)
        actual = GIT.log('--oneline', info=True)
        expected = ['1974b10 Hello there mates', 'c0d1dbb 0']
        self.assertEqual(actual, expected)

        actual = GIT.log('--oneline', 'origin/develop', info=True)
        self.assertEqual(actual, expected)
