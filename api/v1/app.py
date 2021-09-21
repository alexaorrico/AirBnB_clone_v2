#!/usr/bin/python3
"""Module for API"""
from api.v1.views import app_views
from flask import Blueprint, Flask
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(code):
    """handles teardown_appcontext"""
    storage.close()

if __name__ == '__main__':
    host = getenv('HBNB_API_HOST')
    if host is None:
        host = '0.0.0.0'
    port = getenv('HBNB_API_PORT')
    if port is None:
        port = '5000'
    app.run(host, port, threaded=True)
