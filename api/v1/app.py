#!flask/bin/python
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.route('/')
def index():
    return "Hello, World!"


@app.teardown_request
def closee():
    storage.close()


if __name__ == '__main__':
    app.run(host=getenv(
        HBNB_API_HOST),
        port=getenv(HBNB_API_PORT),
        threaded=True)
