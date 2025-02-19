#!/usr/bin/python3
""" App Module """
import os
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint


app = Flask(__name__)


app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown():
    """ Method: Remove the current session """
    storage.close()


if __name__ == "__main__":
    """ Method: Set host and port for usage """
    host = os.getenv("HBNB_API_HOST", default="0.0.0.0")
    port = os.getenv("HBNB_API_PORT", default=5000)
    app.run(host, port, threaded=True)

