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
    #from fortunate.models.sqlalchemy import db
    #db.init_app(app)
    
    from fortunate.models import api
    api.init_app(app)


    # register routes here instead of in __init__ to allow testing
    from fortunate.urls import routes
    for route in routes:
        app.add_url_rule(**route)

    # register exception
    from fortunate.exceptions import ApiException
    app.register_error_handler(ApiException, lambda e: e.to_result())

    return app


class Fortune(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def get_user(self):
        raise NotImplementedError

    def create_user(self):
        raise NotImplementedError
    
    def get_or_create_user(self):
        raise NotImplementedError

    def new_token(self):
        raise NotImplementedError

    def get_key(self):
        raise NotImplementedError

    def create_key(self):
        raise NotImplementedError

    def random_fortune(self):
        raise NotImplementedError
        
    def add_fortune(self):
        raise NotImplementedError

