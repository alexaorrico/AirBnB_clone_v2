#!/usr/bin/python3
"""
A variable app
"""

from flask import Flask, jsoify
from flask_cors import CORS
from os import getenv

from api.v1.views import app_views
from models import storage


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def teardown(exception):
    """
    Teardown functions
    """
    storage.close()

@app.errorhandler(404)
def handle_404(exception):
    """
    Handles 404 errors
    :return: Returns 404 json
    """
    data = {
        "error": "Not found"
    }

    resp = jsonify(data)
    resp.status_code = 404

    return(resp)

    if __name__ == "__main__":
        app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT"))
