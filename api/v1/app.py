#!/usr/bin/python3
"""this is a test string"""

from models import storage
from flask import Flask
from api.v1.views import app_views
from os import getenv
app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.errorhandler(404)
def page_not_found(err=None):
    """this is a test string"""
    return {"error": "Not found"}, 404


@app.teardown_appcontext
def tear(err=None):
    """this is a test string"""
    storage.close()

if __name__ == "__main__":
    h = getenv("HBNB_API_HOST")
    if not h:
        h = "0.0.0.0"
    p = getenv("HBNB_API_PORT")
    if not p:
        p = 5000
    app.run(host=h, port=p, threaded=True)
