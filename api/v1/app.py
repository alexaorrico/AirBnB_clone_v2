#!/usr/bin/python3
"""
Flask API application
"""

from os import getenv

from flask import Flask

from api.v1.views import app_views
from models import storage

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(exception):
    """returns a 404 error"""
    return {"error": "Not found"}, 404


if __name__ == "__main__":
    HBNB_API_HOST = getenv("HBNB_API_HOST", "0.0.0.0")
    HBNB_API_PORT = getenv("HBNB_API_PORT", "5000")
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
