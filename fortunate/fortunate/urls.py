from fortunate.views import TokenAPI, FortuneAPI

routes = [{'rule': '/token/', 'view_func': TokenAPI.as_view('token')},
          {'rule': '/fortune/', 'view_func': FortuneAPI.as_view('fortune')}]
