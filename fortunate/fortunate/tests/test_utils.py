import unittest

from fortunate.utils import make_app

class AppTest(unittest.TestCase):

    def test_app(self):
        app = make_app()
        self.assertEqual(app.name, 'fortunate')

    def test_additional_settings(self):
        class TestSettings:
            TESTCONFIG=True

        app = make_app(TestSettings)
        self.assertTrue(app.config['TESTCONFIG'])
