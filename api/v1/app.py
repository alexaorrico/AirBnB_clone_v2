#!/usr/bin/python3
"""this module contains a Flask APP"""

from api.v1.views import app_views
from flask import Flask
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(self):
    """APP teardown method"""
    storage.close()


if __name__ == "__main__":
    """Initialize APP"""
    app.run(
        host=getenv("HBNB_API_HOST", "0.0.0.0"),
        port=int(getenv("HBNB_API_PORT", "5000")),
        threaded=True)
