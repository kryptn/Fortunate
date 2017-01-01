from random import choice

from flask_sqlalchemy import SQLAlchemy

from fortunate import app

alphanum = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

db = SQLAlchemy(app)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(15))

    def __init__(self, ip):
        self.ip = ip

    @staticmethod
    def get_or_create(ip):
        user = User.query.filter_by(ip=ip).first()
        if user:
            return user

        user = User(ip)
        db.session.add(user)
        db.session.commit()
        return user


class Key(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(16), unique=True)
    private = db.Column(db.Boolean)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('keys', lazy='joined'))

    def __init__(self, user, private=False):
        self.user = user
        result = True
        while result:
            token = ''.join(choice(alphanum) for x in range(16))
            result = Key.query.filter_by(token=token).first()

        self.token = token
        self.private = private

    @staticmethod
    def create(user, private=False):
        key = Key(user, private)
        db.session.add(key)
        db.session.commit()
        return key


class Fortune(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    pulls = db.Column(db.Integer)

    key_id = db.Column(db.Integer, db.ForeignKey('key.id'))
    key = db.relationship('Key', backref=db.backref('fortunes', lazy='joined'))

    def __init__(self, key, text):
        self.text = text
        self.key = key

    @staticmethod
    def get_random(token):
        return Fortune.query.filter(Fortune.key.has(token=token))\
                .order_by(db.func.random()).limit(1).first()
