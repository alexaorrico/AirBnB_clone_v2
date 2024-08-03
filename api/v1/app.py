#!/usr/bin/python3

"""
This is our flask application
"""

from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv

from api.v1.views import app_views
from models import storage


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    This is our teardown function.
    Calls close()
    """
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """
    Handler for 404 error
    Returns 404 json
    """
    data = {
        "error": "Not found"
    }

    resp = jsonify(data)
    resp.status_code = 404

    return (resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
