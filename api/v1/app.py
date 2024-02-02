#!/usr/bin/python3
"""app"""
from flask import Flask
from models import storage
import os
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    "Close connection"
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """ """
    return {'error': 'Not found'}, 404


if __name__ == '__main__':
    API_HOST = os.getenv('HBNB_API_HOST') or '0.0.0.0'
    API_PORT = os.getenv('HBNB_API_PORT') or 5000
    app.run(host=API_HOST, port=API_PORT, threaded=True)
