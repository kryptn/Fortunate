from random import choice

from flask_sqlalchemy import SQLAlchemy

from fortunate import utils
from fortunate.exceptions import ApiException

db = SQLAlchemy()


class SqlFortune(utils.Fortune):

    def init_app(self, app):
        db.init_app(app)

    def commit(self, model):
        db.session.add(model)
        db.session.commit()
        return model

    def get_user(self, ip):
        result = User.query.filter_by(ip=ip).first()
        if result:
            return result
        raise ApiException('IP Not Found')

    def create_user(self, ip):
        return self.commit(User(ip))

    def get_or_create_user(self, ip):
        try:
            return self.get_user(ip)
        except ApiException:
            return self.create_user(ip)

    def get_key(self, token):
        result = Key.query.filter_by(token=token).first()
        if result:
            return result
        raise ApiException('Invalid Token')

    def create_key(self, user):
        return self.commit(Key(user, self.new_token()))

    def random_fortune(self, token):
        result = Fortune.query.filter(Fortune.key.has(token=token))\
                        .order_by(db.func.random()).limit(1).first()
        if result:
            return result
        raise ApiException('Invalid Token or No Fortunes On Token')

    def add_fortune(self, token, text):
        result = Key.query.filter_by(token=token).first()
        key = self.get_key(token)
        return self.commit(Fortune(key, text))

    def new_token(self):
        alphanum = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        result = True
        while result:
            token = ''.join(choice(alphanum) for x in range(16))
            try:
                result = self.get_key(token)
            except Exception:
                result = None
        return token        


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(15))

    def __init__(self, ip):
        self.ip = ip


class Key(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(16), unique=True)
    private = db.Column(db.Boolean)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('keys', lazy='joined'))

    def __init__(self, user, token):
        self.user = user
        self.token = token


class Fortune(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    pulls = db.Column(db.Integer)

    key_id = db.Column(db.Integer, db.ForeignKey('key.id'))
    key = db.relationship('Key', backref=db.backref('fortunes', lazy='joined'))

    def __init__(self, key, text):
        self.text = text
        self.key = key
