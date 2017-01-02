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

class ApiException:
    def __init__(self, message, status=400):
        self.message = message
        self.status = status

    def to_result(self):
        return ApiResult({'message': self.message},
                         status=self.status)

def register_error_handlers(app):
    app.register_error_handler(ApiException, lambda err: err.to_result())

def make_app(additional_settings=None):
    app = ApiFlask('fortunate')
    app.config.from_object('fortunate.default_settings')
    app.config.from_envvar('FORTUNATE_SETTINGS')
    if additional_settings:
        app.config.from_object(additional_settings)

    #register_error_handlers(app)
    return app

