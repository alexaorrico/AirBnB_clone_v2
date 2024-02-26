#!/usr/bin/python3
"""app.py"""
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, Blueprint
import os

HBNB_API_HOST = "0.0.0.0"
HBNB_API_PORT = 5000

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception=None):
    """call close func"""
    storage.close()


@app.errorhandler(404)
def error_handler(e):
    """handle 404 error"""
    return jsonify({"error": "Not found"})


if __name__ == "__main__":
    host = "0.0.0.0" if "HBNB_API_HOST" not in \
            os.environ else os.getenv("HBNB_API_HOST")

    port = 5000 if "HBNB_API_PORT" not in \
        os.environ else os.getenv("HBNB_API_PORT")
    app.run(host=host, port=port, threaded=True, debug=True)
