from string import ascii_letters
from random import choice, sample
from collections import defaultdict

from fortunate.utils import Fortune
from fortunate.exceptions import ApiException


class Dotted:
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class DictFortune(Fortune):

    def __init__(self):
        # Schema:
        #    {username: {token: [fortunes]}}
        self.db = defaultdict(dict)

    def tokens(self):
        t = [v.keys() for k, v in self.db.items()]
        return [x for y in t for x in y]

    def get_user(self, name):
        return self.db[name]

    create_user = get_or_create_user = get_user

    def get_key(self, token):
        bucket = [buckets for user, buckets in self.db.items() if token in buckets]
        if bucket:
            return bucket[0][token]
        raise ApiException('Invalid Token')

    def create_key(self, user):
        token = self.new_token()
        user[token] = []
        return Dotted(token=token)

    def new_token(self):
        result = True
        while result:
            token = ''.join(sample(ascii_letters, 16))
            result = token in self.tokens()
        return token

    def random_fortune(self, token):
        fortunes = self.get_key(token)
        if fortunes:
            return Dotted(text=choice(fortunes))
        raise ApiException('Invalid Token or No Fortunes')

    def add_fortune(self, token, text):
        bucket = self.get_key(token)
        bucket.append(text)
        return Dotted(text=text)

        
