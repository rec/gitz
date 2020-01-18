from gitz.git import combine
import unittest


class ShuffleTest(unittest.TestCase):
    def test_identity(self):
        self.assertEqual(combine.permutation('a'), [])
        self.assertEqual(combine.permutation('ab'), [])
        self.assertEqual(combine.permutation('abc'), [])

        self.assertEqual(combine.permutation('a', True), [0, 1])
        self.assertEqual(combine.permutation('ab', True), [0, 1, 2])
        self.assertEqual(combine.permutation('abc', True), [0, 1, 2, 3])

    def test_swap(self):
        self.assertEqual(combine.permutation('ba'), [1, 0, 2])

    def test_cycle(self):
        self.assertEqual(combine.permutation('cab'), [2, 0, 1, 3])
        self.assertEqual(combine.permutation('cabe'), [2, 0, 1, 4])
        self.assertEqual(combine.permutation('dbcf'), [3, 1, 2, 5])
        self.assertEqual(combine.permutation('ebcg'), [4, 1, 2, 6])
        self.assertEqual(combine.permutation('hfgj'), [7, 5, 6, 9])

    def test_cleaning(self):
        self.assertEqual(combine.permutation('cabdef'), [2, 0, 1, 3])
        self.assertEqual(combine.permutation('cabedf'), [2, 0, 1, 4, 3, 5])
        self.assertEqual(combine.permutation('abcdfe'), [0, 1, 2, 3, 5, 4, 6])
