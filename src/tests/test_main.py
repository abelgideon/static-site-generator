import unittest

from main import extract_title


class TestMain(unittest.TestCase):
    def test_extract_title(self):
        res = extract_title("#         Hello   ")
        self.assertEqual(res, "Hello")
