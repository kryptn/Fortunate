from random import choice

from flask import Flask, json, Response, request
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy




class ApiFlask(Flask):
    def make_response(self, rv):
        if isinstance(rv, ApiResult):
            return rv.to_response()
        return Flask.make_response(self, rv)


class ApiResult:
    def __init__(self, value, status=200):
        self.value = value
        self.status = status

    def to_response(self):
        return Response(json.dumps(self.value),
                        status=self.status,
                        mimetype='application/json')


class ApiException(Exception):
    def __init__(self, message, status=400):
        Exception.__init__(self)
        self.message = message
        self.status = status

    def to_result(self):
        return ApiResult({'message': self.message},
                         status=self.status)


app = ApiFlask(__name__)
app.config.from_object('prod')
db = SQLAlchemy(app)


class FortuneApi:
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

api = FortuneApi()

class TokenAPI(MethodView):
    def get(self):
        user = api.get_or_create_user(request.remote_addr)
        key = api.create_key(user)
        return ApiResult({'token':key.token})


class FortuneAPI(MethodView):
    def get(self):
        token = request.form.get('token', None)
        if not token:
            raise ApiException('Token Required')
        
        fortune = api.random_fortune(token)
        return ApiResult({'fortune':fortune.text})

    def post(self):
        token = request.form.get('token', None)
        fortune = request.form.get('fortune', None)
        if not token or not fortune:
            raise ApiException('Token and Fortune Required')
        fortune = api.add_fortune(token, fortune)
        return ApiResult({'fortune':fortune.text})


routes = [{'rule': '/', 'view_func': lambda: "Hello World"},
          {'rule': '/token/', 'view_func': TokenAPI.as_view('token')},
          {'rule': '/fortune/', 'view_func': FortuneAPI.as_view('fortune')}]

for route in routes:
    app.add_url_rule(**route)


@app.route('/mkdb')
def makedb():
    db.create_all()


app.register_error_handler(ApiException, lambda e: e.to_result())

if __name__ == '__main__':
    app.run()
