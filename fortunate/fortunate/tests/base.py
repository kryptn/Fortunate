from flask_testing import TestCase
from fortunate.utils import make_app
from fortunate.models.sqlalchemy import db

class Base(TestCase):
    
    def create_app(self):
        app = make_app('fortunate.test_settings')
        app.add_url_rule('/', view_func=lambda: 'test')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

