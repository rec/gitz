from . import repo
from gitz.runner import GIT_INFO
import unittest


class GitAmpTest(unittest.TestCase):
    @repo.test
    def test_simple(self):
        repo.make_commit('1')
        GIT_INFO.checkout('-b', 'develop')

        GIT_INFO.push('--set-upstream', 'origin', 'develop')
        GIT_INFO.amp('Hello', 'there', 'mates')
        actual = GIT_INFO.log('--oneline')
        expected = ['1974b10 Hello there mates', 'c0d1dbb 0']
        self.assertEqual(actual, expected)

        actual = GIT_INFO.log('--oneline', 'origin/develop')
        self.assertEqual(actual, expected)
