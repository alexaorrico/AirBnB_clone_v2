#!/usr/bin/python3
<<<<<<< HEAD
"""Initializing Blueprint"""

from api.v1.views.index import *
from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
=======

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
>>>>>>> 59833b06c41e32f80b156b217b0a0f332b30db4f
