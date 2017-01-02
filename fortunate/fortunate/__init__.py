from flask import Flask

def make_app(additional_settings=None):
    app = Flask(__name__)
    app.config.from_object('fortunate.default_settings')
    app.config.from_envvar('FORTUNATE_SETTINGS')
    if additional_settings:
        app.config.from_object(additional_settings)

    return app

app = make_app()

from fortunate.models import db, User, Key, Fortune
