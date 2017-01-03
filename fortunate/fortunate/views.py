
from flask import request
from flask.views import MethodView


from fortunate.models import User, Key, Fortune
from fortunate.utils import ApiResult, ApiException

class TokenAPI(MethodView):
    def get(self):
        user = User.get_or_create(request.remote_addr)
        key = Key.create(user)
        return ApiResult({'token':key.token})

class FortuneAPI(MethodView):
    def get(self):
        token = request.form.get('token', None)
        if token:
            fortune = Fortune.get_random(token)
            if fortune:
                return ApiResult({'fortune':fortune.text})
            return ApiException('Invalid Token or No Fortune')
        return ApiException('token required')

    def post(self):
        token = request.form.get('token', None)
        fortune = request.form.get('fortune', None)
        if token and fortune:
            key = Key.query.filter_by(token=token).first()
            if key:
                result = Fortune.add(key, fortune)
                return ApiResult({'fortune': result.text})
            return ApiException('Invalid Token')
        return ApiException('Malformed Request (token and fortune required)')
