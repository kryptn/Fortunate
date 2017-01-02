import unittest

from fortunate import db, models

from base import Base

class ModelsTest(Base):

    def test_user_create(self):
        u = models.User.get_or_create('1.1.1.1')
        self.assertEqual(u.id, 1)

    def test_user_get_if_exists(self):
        u_create = models.User.get_or_create('1.1.1.1')
        u_get = models.User.get_or_create('1.1.1.1')
        self.assertEqual(u_create, u_get)

    def test_user_key(self):
        u = models.User.get_or_create('1.1.1.1')
        k = models.Key.create(u)
        self.assertEqual(k.user, u)
        self.assertEqual(u.keys[0], k)

    def test_add_fortune(self):
        u = models.User.get_or_create('1.1.1.1')
        k = models.Key.create(u)
        fortune_text = 'fortune'
        f = models.Fortune.add(k, fortune_text)
        self.assertEqual(f.id, 1)
        self.assertEqual(f.text, fortune_text)

    def test_random_fortune(self):
        u = models.User.get_or_create('1.1.1.1')
        k = models.Key.create(u)
        first_fortune = 'fortune1'
        second_fortune = 'fortune2'
        f1 = models.Fortune.add(k, first_fortune)
        f2 = models.Fortune.add(k, second_fortune)
        
        self.assertTrue(models.Fortune.get_random(k.token).id in [1, 2])

    def test_random_isolated_fortune(self):        
        u = models.User.get_or_create('1.1.1.1')
        k = models.Key.create(u)
        k2 = models.Key.create(u)
        first_fortune = 'fortune1'
        second_fortune = 'fortune2'
        f1 = models.Fortune.add(k, first_fortune)
        f2 = models.Fortune.add(k2, second_fortune)

        self.assertNotEqual(models.Fortune.get_random(k.token).id, 2)




