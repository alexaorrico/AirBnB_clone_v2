#!/usr/bin/python3
"""Module app flask"""
from models import storage
from flask import Blueprint, Flask
from os import environ
from api.v1.views import app_views

env = environ.copy()

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """close storage"""
    storage.close()

if __name__ == '__main__':
    if "HBNB_API_HOST" in env:
        host_api = env['HBNB_API_HOST']
    else:
        host_api = '0.0.0.0'
    if 'HBNB_API_PORT' in env:
        host_port = env['HBNB_API_PORT']
    else:
        host_port = 5000
    app.run(host=host_api, port=host_port, threaded=True)
