#!/usr/bin/python3
"""
Module for the main Flask application.
"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    Tears down the app context, closes the storage.
    """
    storage.close()


if __name__ == "__main__":
    host = "0.0.0.0" if not getenv(
        "HBNB_API_HOST") else getenv("HBNB_API_HOST")
    port = 5000 if not getenv(
        "HBNB_API_PORT") else int(getenv("HBNB_API_PORT"))
    app.run(host=host, port=port, threaded=True)
