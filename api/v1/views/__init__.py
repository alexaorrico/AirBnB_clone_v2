#!/usr/bin/python3

from flask import Flask, Blueprint
from os import environ
from models import storage
from api.v1.views import *


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def close_storage(error):
    """closes the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    port = environ.get('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
