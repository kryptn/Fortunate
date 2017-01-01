from flask import Flask

app = Flask(__name__)
app.config.from_object('fortunate.settings')

from fortunate.models import User, Key, Fortune

if __name__ == '__main__':
    pass
