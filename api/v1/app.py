#!/usr/bin/python3
""" API application"""

from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views
import os

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def closeDB(arg):
    """
    method to close the storage connection
    """
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """
    method to handle 404 errors
    """
    return (jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')
    host = host if host is not None else "0.0.0.0"
    port = port if port is not None else 5000
    app.run(host=host, port=port, threaded=True, debug=True)
