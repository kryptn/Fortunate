from fortunate import models, views

from fortunate.tests.base import Base

class ViewsTest(Base):

    def test_token_get(self):
        response = self.client.get('/token/')
        self.assert200(response)
        self.assertEqual(len(response.json['token']), 16)

    def test_fortune_post(self):
        pass

    def test_fortune_get(self):
        pass
