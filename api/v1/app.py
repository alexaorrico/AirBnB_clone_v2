#!/usr/bin/python3
"""
main file to run all the flask blueprinted apps concurrently
"""

from flask import Flask, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views
from flask_cors import CORS

API_HOST = str(getenv('HBNB_API_HOST', '0.0.0.0'))
API_PORT = int(getenv('HBNB_API_PORT', '5000'))

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "0.0.0.0"
    }
})

app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def close_storage(exception=None):
    """
    If HBNB_TYPE_STORAGE=db closes current session
    If HBNB_TYPE_STORAGE=file reloads file and deserialises JSON objects
    """
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    """
    Handles the Page Not Found Error by returning JSON and 404 error code
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=API_HOST, port=API_PORT, threaded=True)
