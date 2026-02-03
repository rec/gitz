import unittest

from gitz_doc import clean_manpage


class CleanManpageTest(unittest.TestCase):
    def test_simple(self):
        actual = clean_manpage.clean_line('')
        expected = ''
        self.assertEqual(actual, expected)

    def test_code(self):
        actual = clean_manpage.clean_line('The word ``moo``.')
        expected = r'The word \fBmoo\fP.'
        self.assertEqual(actual, expected)

        actual = clean_manpage.clean_line('The word `moo`')
        expected = r'The word \fBmoo\fP'
        self.assertEqual(actual, expected)
