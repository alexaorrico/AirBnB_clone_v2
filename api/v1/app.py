#!/usr/bin/python3
""" script that runs flask """
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """ calls storage.close() """
    storage.close()


if __name__ == '__main__':
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')

    if not HBNB_API_HOST:
        host = '0.0.0.0'
    else:
        host = HBNB_API_HOST

    if not HBNB_API_PORT:
        port = 5000
    else:
        port = HBNB_API_PORT
    app.run(host=host, port=port, threaded=True)
