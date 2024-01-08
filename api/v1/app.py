#!/usr/bin/python3
"""
this module is to use CORs for api testing
"""
from api.v1.views import app_views
import sys
from flask import Flask, jsonify
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Calls storage.close() upon teardown."""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors and returns a JSON-formatted response."""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', threaded=True)
