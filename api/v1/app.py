#!/usr/bin/python3
"""creates a variable app, instance of flask, and tears down"""

from flask import Flask
from api.v1.views import app_views
from models import storage
import os
from flask import jsonify

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception=None):
    """Closes a session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """returns a json string of error 404"""
    return jsonify({"error":  "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
