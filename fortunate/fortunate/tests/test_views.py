from fortunate import models, views

from fortunate.tests.base import Base

class ViewsTest(Base):
    
    fortunes = list('abcdefg')

    def set_fortune(self, *args, **kwargs):
        payload = kwargs
        response = self.client.post('/fortune/', data=payload)
        return response                

    def test_token_get(self):
        response = self.client.get('/token/')
        self.assert200(response)
        self.assertEqual(len(response.json['token']), 16)

    def test_fortune_post(self):
        response = self.client.get('/token/')
        result = self.set_fortune(token=response.json['token'], fortune=self.fortunes[0])

        self.assert200(result)
        self.assertEqual('a', result.json['fortune'])

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

    def test_fortune_get_invalid_token(self):
        result = self.client.get('/fortune/', data={'token': 'x'})

        self.assert400(result)
        self.assertTrue('Invalid' in result.json['message'])

    def test_fortune_get_empty_fortune(self):
        token = self.client.get('/token/')
        result = self.client.get('/fortune/', data={'token': token.json['token']})

        self.assert400(result)
        self.assertTrue('Fortune' in result.json['message'])
