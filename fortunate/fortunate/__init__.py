from fortunate.utils import make_app

app = make_app()

from fortunate.models import db, User, Key, Fortune

from fortunate.views import TokenAPI, FortuneAPI

app.add_url_rule('/token/', view_func=TokenAPI.as_view('token'))
app.add_url_rule('/fortune/', view_func=FortuneAPI.as_view('fortune'))
