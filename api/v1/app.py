#!/usr/bin/python3
"""a module as an API"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)


@app.teardown_appcontext
def close_storage():
    """a function to call storage.close()"""
    storage.close()


if __name__ == "__main__":
    api_host = getenv("HBNB_API_HOST", "0.0.0.0")
    api_port = int(getenv("HBNB_API_PORT", "5000"))
    app.run(host=api_host, port=api_port, threaded=True)
