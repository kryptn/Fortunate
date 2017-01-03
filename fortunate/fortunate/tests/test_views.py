from fortunate import models, views

from fortunate.tests.base import Base

class ViewsTest(Base):
    
    fortunes = list('abcdefg')

    def set_fortune(self, token, fortune):
        payload = {'token': token, 'fortune': fortune}
        response = self.client.post('/fortune/', data=payload)
        return response                

    def test_token_get(self):
        response = self.client.get('/token/')
        self.assert200(response)
        self.assertEqual(len(response.json['token']), 16)

    def test_fortune_post(self):
        response = self.client.get('/token/')
        result = self.set_fortune(response.json['token'], self.fortunes[0])

        self.assert200(result)
        self.assertEqual('a', result.json['fortune'])

    def test_fortune_get(self):
        response = self.client.get('/token/')
        result = self.set_fortune(response.json['token'], self.fortunes[0])
        fortune = self.client.get('/fortune/', data={'token': response.json['token']})
        
        self.assert200(fortune)
        self.assertEqual('a', fortune.json['fortune'])

    def test_fortune_get_random(self):
        token = self.client.get('/token/').json
        results = [self.set_fortune(token['token'], x) for x in self.fortunes]

        fortune = self.client.get('/fortune/', data=token)

        self.assert200(fortune)
        self.assertTrue(fortune.json['fortune'] in self.fortunes)
