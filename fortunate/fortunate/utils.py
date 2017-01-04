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
                        status = self.status,
                        mimetype='application/json')


class ApiException(Exception):
    def __init__(self, message, status=400):
        Exception.__init__(self)
        self.message = message
        self.status = status

    def to_result(self):
        return ApiResult({'message': self.message},
                         status=self.status)


def make_app(additional_settings=None):
    app = ApiFlask('fortunate')
    app.config.from_object('fortunate.default_settings')
    if additional_settings:
        app.config.from_object(additional_settings)

    # initialize db connection to avoid circular import
    from fortunate.models import db
    db.init_app(app)

    # register routes here instead of in __init__
    from fortunate.urls import routes
    for route in routes:
        app.add_url_rule(**route)

    app.register_error_handler(ApiException, lambda e: e.to_result())

    return app

