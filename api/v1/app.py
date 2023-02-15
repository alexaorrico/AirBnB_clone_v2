#!/usr/bin/python3
"""
This module creates and configures the Flask application.
"""

from os import environ
from flask import Flask, Blueprint
from api.v1.views import app_views
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown(exception):
    """
    Call the close method of the storage object
    """
    storage.close()


if __name__ == "__main__":
    host = environ.get("HBNB_API_HOST", "0.0.0.0")
    port = environ.get("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
