from random import choice

from flask import Flask, json, Response


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


def make_app(additional_settings=None):
    app = ApiFlask('fortunate')
    app.config.from_object('fortunate.default_settings')
    if additional_settings:
        app.config.from_object(additional_settings)

    # initialize db connection to avoid circular import
    from fortunate.models.sqlalchemy import db
    db.init_app(app)

    # register routes here instead of in __init__ to allow testing
    from fortunate.urls import routes
    for route in routes:
        app.add_url_rule(**route)

    # register exception
    from fortunate.exceptions import ApiException
    app.register_error_handler(ApiException, lambda e: e.to_result())

    return app


class Fortune:

    def get_user(self):
        raise NotImplemented

    def create_user(self):
        raise NotImplemented

    def get_or_create_user(self, *args, **kwargs):
        try:
            return self.get_user(*args, **kwargs)
        except Exception:
            return self.create_user(*args, **kwargs)

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

    def get_key(self):
        raise NotImplemented

    def create_key(self):
        raise NotImplemented

    def random_fortune(self):
        raise NotImplemented
        
    def add_fortune(self):
        raise NotImplemented

