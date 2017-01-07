from flask import g

from fortunate.utils import Fortune
from fortunate.models.sqlalchemy import SqlFortune
from fortunate.models.dict import DictFortune

api = Fortune()

def init_api(backend, app):
    global api
    if backend == 'sql':
        api = SqlFortune()
    else:
        api = DictFortune()

    api.init_app(app)



