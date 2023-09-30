#!/usr/bin/python3
"""Instantiate a Flask application"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

# create flask instance
app = Flask(__name__)

# register blueprint app_views
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(error):
    """close open storage session after a request"""
    storage.close()


if __name__ == "__main__":
    """launch the flask instance"""
    ht = getenv("HBNB_API_HOST", "0.0.0.0")
    pt = int(getenv("HBNB_API_PORT", "5000"))
    app.run(host=ht, port=pt, threaded=True)
