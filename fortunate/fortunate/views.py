from flask import request, current_app, g
from flask.views import MethodView
from werkzeug.local import LocalProxy

from fortunate.exceptions import ApiException
from fortunate.models import api
from fortunate.utils import ApiResult

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

