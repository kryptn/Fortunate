import unittest

from flask_testing import TestCase
from fortunate import make_app, db, models

class ModelsTest(TestCase):

    def create_app(self):
        return make_app()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_test(self):
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
