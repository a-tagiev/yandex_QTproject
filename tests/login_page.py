import unittest

from logics import LoginPage


class TestLoginPage(unittest.TestCase):
    def test_empty_user(self):
        self.assertEqual(LoginPage.username, not None)
