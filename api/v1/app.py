#!/usr/bin/python3
"""
Start flask app
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import environ


app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


if __name__ == "__main__":
    """ Main Function """
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
