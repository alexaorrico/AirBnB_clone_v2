#!/usr/bin/python3
"""
    Start of API module
"""

from flask import Flask, escape, request, Blueprint
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def close(self):
    """ Calls the close method from storage """
    storage.close()

if __name__ == "__main__":
    """ Only executes as main """
    api_host = getenv("HBNB_API_HOST")
    if not api_host:
        api_host = "0.0.0.0"
    api_port = getenv("HBNB_API_PORT")
    if not api_port:
        api_port = "5000"
    app.run(host=api_host, port=api_port, threaded=True)
