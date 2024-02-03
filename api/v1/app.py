#!/usr/bin/python3
"""Entry point of the api"""
from flask import Flask, abort
import os

from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.url_map.strict_slashes = False

app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(e):
    """404 error Handler"""
    abort(404)


@app.teardown_appcontext
def teardown(exception):
    "Close connection"
    storage.close()


if __name__ == '__main__':
    API_HOST = os.getenv('HBNB_API_HOST') or '0.0.0.0'
    API_PORT = os.getenv('HBNB_API_PORT') or 5000
    app.run(host=API_HOST, port=API_PORT, threaded=True)
