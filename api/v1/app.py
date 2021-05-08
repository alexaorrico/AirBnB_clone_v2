#!/usr/bin/python3
"""app.py"""
from models import storage
from api.v1.views import app_views
from flask import Flask
from os import getenv

app = Flask('app')

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext:
    """teardown_appcontext"""
    storage.close()

if __name__ "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
