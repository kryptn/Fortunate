
from random import choice

from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fortunes.db'
db = SQLAlchemy(app)
api = Api(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    ip = db.Column(db.String(15))

    def __init__(self, ip):
        self.ip = ip

    def get_or_create(self, ip):
        user = User.query.filter_by(ip=ip).first()
        if user:
            return user

        user = User(ip)
        db.session.add(user)
        db.session.commit()
        return user


class Key(db.Model):
    
    alphanum = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(16), unique=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('keys', lazy='joined'))

    def __init__(self, user):
        self.user = user
        result = True
        while result:
            token = ''.join(choice(self.alphanum) for x in range(16))
            result = Key.query.filter_by(token=token).first()

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


class KeyView(Resource):
    def get(self):
        pass

class FortuneView(Resource):
    def get(self):
        return 'thing'

    def put(self):
        token = request.form.get('token', None)

        if token:
            key = Key.query.filter_by(token=token).first()
            if key:
                fortunes = []
                raw_str = request.form.get('fortune', None)
                raw_list = request.form.get('fortunes', None)
                if raw_str:
                    fortunes.append(raw_str)
                elif raw_list:
                    fortunes += raw_list
                else:
                    pass # return some http empty status

                db.session.add_all(Fortune(key, f) for f in fortunes)
            else:
                pass # token invalid
        else:
            pass # Key Required        

