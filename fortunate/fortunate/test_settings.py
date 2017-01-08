
class test_sql(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FORTUNATE_BACKEND = 'sql'
    TESTING = True

class test_dict(object):
    TESTING = True
    FORTUNATE_BACKEND = 'dict'
