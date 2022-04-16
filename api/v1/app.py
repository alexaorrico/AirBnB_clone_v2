#!/usr/bin/python3
""" import necesaary modules for variable app.py"""
from flask import Flask
from models import storage
from os import getenv
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slaches = False


@app.teardown_appcontext
def call_storage(self):
    """method to call storage.close()"""
    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
