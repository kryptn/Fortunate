from flask import request
from flask.views import MethodView

#from fortunate.models.sqlalchemy import SqlFortune
from fortunate.models.dict import DictFortune
from fortunate.exceptions import ApiException
from fortunate.utils import ApiResult

#api = SqlFortune()
api = DictFortune()

# logic for initilizing storage would go here
# fortunate.utils.make_app would set it to the app instance
# probably something like `api = flask.current_app.storage()`

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

