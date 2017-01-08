from flask_testing import TestCase

from fortunate.utils import make_app

class ViewsMixin(object):
    fortunes = list('abcdefg')

    def set_fortune(self, *args, **kwargs):
        payload = kwargs
        response = self.client.post('/fortune/', data=payload)
        return response                

    def test_token_get(self):
        #import pdb; pdb.set_trace()
        response = self.client.get('/token/')
        self.assert200(response)
        self.assertEqual(len(response.json['token']), 16)

        response = self.client.get('/token/')
        self.assert200(response)

    def test_fortune_post(self):
        response = self.client.get('/token/')
        result = self.set_fortune(token=response.json['token'], fortune=self.fortunes[0])

        self.assert200(result)
        self.assertEqual('a', result.json['fortune'])

        result = self.set_fortune(token=response.json['token'], fortune=self.fortunes[1])
        self.assert200(result)

    def test_fortune_post_empty(self):
        response = self.client.get('/token/')
        result = self.set_fortune(token=response.json['token'])

        self.assert400(result)
        self.assertTrue('Required' in result.json['message'])

    def test_fortune_post_invalid_token(self):
        result = self.set_fortune(token='x', fortune='x')
        self.assert400(result)
        self.assertTrue('Invalid' in result.json['message'])

    def test_fortune_get(self):
        response = self.client.get('/token/')
        result = self.set_fortune(token=response.json['token'], fortune=self.fortunes[0])
        fortune = self.client.get('/fortune/', data={'token': response.json['token']})
        
        self.assert200(fortune)
        self.assertEqual('a', fortune.json['fortune'])

    def test_fortune_get_random(self):
        token = self.client.get('/token/').json
        results = [self.set_fortune(token=token['token'], fortune=x) for x in self.fortunes]

        fortune = self.client.get('/fortune/', data=token)

        self.assert200(fortune)
        self.assertTrue(fortune.json['fortune'] in self.fortunes)

    def test_fortune_get_empty_token(self):
        response = self.client.get('/token/')
        result = self.set_fortune(token=response.json['token'], fortune=self.fortunes[0])
        fortune = self.client.get('/fortune/', data={'token': None})
        
        self.assert400(fortune)
        self.assertTrue('Required' in fortune.json['message'])

    def test_fortune_get_invalid_token(self):
        result = self.client.get('/fortune/', data={'token': 'x'})

        self.assert400(result)
        self.assertTrue('Invalid' in result.json['message'])

    def test_fortune_get_empty_fortune(self):
        token = self.client.get('/token/')
        result = self.client.get('/fortune/', data={'token': token.json['token']})

        self.assert400(result)
        self.assertTrue('Fortune' in result.json['message'])

    def test_index(self):
        resp = self.client.get('/')
        self.assert200(resp)

class TestSqlViews(TestCase, ViewsMixin):    
    def create_app(self):
        app = make_app('fortunate.test_settings.test_sql')
        app.add_url_rule('/', view_func=lambda: 'test')
        return app

    def setUp(self):
        from fortunate.models.sqlalchemy import db

        db.create_all()

    def tearDown(self):
        from fortunate.models.sqlalchemy import db
        db.session.remove()
        db.drop_all()


#class TestDictViews(TestCase, ViewsMixin):
#    def create_app(self):
#        app = make_app('fortunate.test_settings.test_dict')
#        app.add_url_rule('/', view_func=lambda: 'test')
#        return app
