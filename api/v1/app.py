#!/usr/bin/python3
""" Module for the API """
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown(self):
    """Method to close the session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Method to handle 404 errors"""
    return {"error": "Not found"}, 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    if not host:
        host = "0.0.0.0"
    if not port:
        port = 5000
    app.run(host=host, port=port, threaded=True)
