#!/usr/bin/python3
"""Starts a Flask Application"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    if host and port:
        app.run(host=host, port=port, threaded=True)
    else:
        app.run(host="0.0.0.0", port=5000, threaded=True)


@app.teardown_appcontext
def tear_down():
    """closes the session on after a request"""
    storage.close()
