import unittest

from fortunate.utils import make_app, Fortune


class AppTest(unittest.TestCase):

    def test_app(self):
        app = make_app()
        self.assertEqual(app.name, 'fortunate')

    def test_sql_backend(self):
        app = make_app('fortunate.test_settings.test_sql')        
        self.assertEqual(app.config.get('FORTUNATE_BACKEND'), 'sql')

    def test_dict_backend(self):
        app = make_app('fortunate.test_settings.test_dict')
        self.assertTrue('FORTUNATE_BACKEND' in app.config)

    def test_additional_settings(self):
        class TestSettings:
            TESTCONFIG=True

        app = make_app(TestSettings)
        self.assertTrue(app.config['TESTCONFIG'])


class FortuneTest(unittest.TestCase):

    def setUp(self):
        self.f = Fortune()

    def test_get_user(self):
        self.assertRaises(NotImplementedError, self.f.get_user)

    def test_create_user(self):
        self.assertRaises(NotImplementedError, self.f.create_user)

    def test_get_or_create_user(self):
        self.assertRaises(NotImplementedError, self.f.get_or_create_user)

    def test_new_token(self):
        self.assertRaises(NotImplementedError, self.f.new_token)

    def test_get_key(self):
        self.assertRaises(NotImplementedError, self.f.get_key)

    def test_create_key(self):
        self.assertRaises(NotImplementedError, self.f.create_key)

    def test_random_fortune(self):
        self.assertRaises(NotImplementedError, self.f.random_fortune)

    def test_add_fortune(self):
        self.assertRaises(NotImplementedError, self.f.add_fortune)
 
