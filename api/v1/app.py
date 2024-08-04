#!/usr/bin/python3
"""
Flask app
"""

from api.v1.views import app_views
from models import storage
from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    Function to destroy a session
    """
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """
    Function that handles 404 error
    :return: return error in JSON format
    """
    data = {
        "error": "Not found"
    }

    resp = jsonify(data)
    resp.status_code = 404

    return (resp)



if __name__ == "__main__":
    app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT"))
