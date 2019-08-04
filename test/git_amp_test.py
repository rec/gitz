from . import repo
from gitz.program import PROGRAM
import unittest


class GitAmpTest(unittest.TestCase):
    @repo.test
    def test_simple(self):
        repo.make_commit('1')
        PROGRAM.git.checkout('-b', 'develop')

        PROGRAM.git.push('--set-upstream', 'origin', 'develop')
        PROGRAM.git.amp('Hello', 'there', 'mates')
        actual = PROGRAM.git.log('--oneline')
        expected = ['1974b10 Hello there mates', 'c0d1dbb 0']
        self.assertEqual(actual, expected)

        actual = PROGRAM.git.log('--oneline', 'origin/develop')
        self.assertEqual(actual, expected)
