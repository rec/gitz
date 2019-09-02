
from . import repo
from gitz.program import git
import unittest


class GitUpdateTest(unittest.TestCase):
    @repo.test
    def test_update(self):
        repo.make_one_commit('file.txt', ORIGINAL, 'original')
        repo.make_one_commit('file.txt', DELTA3, 'master!')
        git.push('--set-upstream', 'upstream', 'master')
        git.reset('--hard', 'HEAD~')
        git.push('--set-upstream', 'origin', 'master')

        # No conflicts
        git.fresh('one')
        repo.make_commit('one')
        git.push()

        # Resolvable conflict
        git.fresh('two')
        repo.make_one_commit('file.txt', DELTA1, 'two')
        git.push()

        # Unresolvable conflict
        # TODO: this didn't work
        git.fresh('three')
        repo.make_one_commit('file.txt', DELTA2, 'three')
        git.push()

        # Local differs from origin
        git.fresh('four')
        repo.make_one_commit('file.txt', 'four', 'four')

        git.checkout('master')
        git.update('-v')

        base = ['d1b2fc8 master!', '28da9aa original', 'c0d1dbb 0']

        def test(branch, *items):
            actual = git.log('--oneline', branch)
            expected = list(items) + base
            self.assertEqual(expected, actual)

        test('master')
        test('origin/master')
        test('upstream/master')

        test('one', '2b7979a one')
        test('origin/one', '2b7979a one')

        test('two', '5478a38 two')
        test('origin/two', '5478a38 two')

        test('three', '6158500 three')
        test('origin/three', '6158500 three')

        test('four', '62584d2 four')
        test('origin/four', '62584d2 four')


ORIGINAL = """\
1. hello world
2. line 2
3. line 3
"""
DELTA1 = """\
1. hello DELTA
2. line 2
3. line 3
"""
DELTA2 = """\
1. hello world
2. line DELTA
3. line 3
"""
DELTA3 = """\
1. hello world
2. line NOT-DELTA
3. line 3
"""
