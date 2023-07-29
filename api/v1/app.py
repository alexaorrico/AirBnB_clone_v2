#!/usr/bin/python3

"""Api Interface"""
from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def tearDown(exc):
    """Close the session and request a new one once the application context is
    poped"""
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    if port and host:
        app.run(host=host, port=int(port), threaded=True)
