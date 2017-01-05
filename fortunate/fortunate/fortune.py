

class Fortune:
    def get_user(self):
        raise NotImplemented

    def create_user(self):
        raise NotImplemented

    def get_or_create_user(self, *args, **kwargs):
        result = self.get_user(*args, **kwargs)
        if result:
            return result
        return self.create_user(*args, **kwargs)

    def get_key_token(self):
        raise NotImplemented

    def create_key(self):
        raise NotImplemented

    def random_fortune(self):
        raise NotImplemented
        
    def add_fortune(self):
        raise NotImplemented

