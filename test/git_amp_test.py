from . import repo
from gitz.git import GIT
import unittest


class GitAmpTest(unittest.TestCase):
    @repo.method
    def test_simple(self):
        repo.make_commit('1')
        GIT.checkout('-b', 'develop')

        GIT.push('--set-upstream', 'origin', 'develop')
        GIT.amp('Hello', 'there', 'mates')
        actual = GIT.log('--oneline')
        expected = ['1974b10 Hello there mates', 'c0d1dbb 0']
        self.assertEqual(actual, expected)

        actual = GIT.log('--oneline', 'origin/develop')
        self.assertEqual(actual, expected)
