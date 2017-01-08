from flask import g

from fortunate.utils import Fortune
from fortunate.models.sqlalchemy import SqlFortune
from fortunate.models.dict import DictFortune
from werkzeug.local import LocalProxy


backends = {'sql': SqlFortune,
            'dict': DictFortune}

api = SqlFortune()

def init_api(backend, app):
    g._fortunate_api = backends[backend](app)



