#!/usr/bin/python3
"""Application module"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
host = getenv("HBNB_API_HOST")
port = getenv("HBNB_API_PORT")


@app.teardown_appcontext
def tear_down(self):
    """closes query after each session"""
    storage.close()


if __name__ == "__main__":
    host = '0.0.0.0' if host is None else host
    port = '5000' if port is None else port

    app.run(host, port, threaded=True)
