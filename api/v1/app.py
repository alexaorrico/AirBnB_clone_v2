#!/usr/bin/python3
"""
app.py module
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def storage_close(exception):
    """close"""
    storage.close()


@app.error_handler(404)
def error_handler(exception):
    """handle 404 error"""
    return jsonify({"error": "Not found"})


if __name__ == "__main__":
    hosting = getenv("HBNB_API_HOST", "0.0.0.0")
    porting = getenv("HBNB_API_PORT", "5000")
    app.run(host=hosting, port=porting, threaded=True)
