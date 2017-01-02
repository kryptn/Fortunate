from flask_testing import TestCase
from fortunate import make_app, db

class Base(TestCase):
    
    def create_app(self):
        return make_app()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

