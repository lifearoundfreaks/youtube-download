import unittest
from video import validate_url


class TestUrlValidation(unittest.TestCase):

    def test_ampersand_splitting(self):

        correct_result = 'https://www.youtube.com/watch?v=1Lfv5tUGsn8'

        self.assertEqual(validate_url(
            'https://www.youtube.com/watch?v=1Lfv5tUGsn8'
            '&list=TLPQMTMwNDIwMjHlkFY9B3CuTQ&index=1'
        ), correct_result)

        self.assertEqual(validate_url(
            'https://www.youtube.com/watch?v=1Lfv5tUGsn8&'
        ), correct_result)

        self.assertEqual(validate_url(
            'https://www.youtube.com/watch?v=1Lfv5tUGsn8'
        ), correct_result)
