from gitz.git import GIT
from gitz.git import repo
import unittest


class GitUpdateTest(unittest.TestCase):
    @repo.test
    def test_update(self):
        first = repo.make_one_commit('file.txt', ORIGINAL, 'original')
        self.assertEqual(first, '28da9aa')

        second = repo.make_one_commit('file.txt', DELTA3, 'master!')
        self.assertEqual(second, 'd1b2fc8')

        GIT.push('--set-upstream', 'upstream', 'master')
        GIT.reset('--hard', 'HEAD~')
        GIT.push('--set-upstream', 'origin', 'master')

        # No conflicts
        GIT.new('one')
        repo.make_commit('one')
        GIT.push()

        # Resolvable conflict
        GIT.new('two')
        repo.make_one_commit('file.txt', DELTA1, 'two')
        GIT.push()

        # Unresolvable conflict
        # TODO: this didn't work
        GIT.new('three')
        repo.make_one_commit('file.txt', DELTA2, 'three')
        GIT.push()

        # Local differs from origin
        GIT.new('four')
        repo.make_one_commit('file.txt', 'four', 'four')

        GIT.checkout('master')
        GIT.update('-v')

        lines = [first + ' original', 'c0d1dbb 0']

        def test(branch, *items):
            actual = GIT.log('--oneline', branch)
            expected = list(items) + lines
            self.assertEqual(expected, actual)

        test('master')
        test('origin/master')

        lines.insert(0, second + ' master!')

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
