#!/usr/bin/python3
"""
This script runs a Flask API.
"""
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', '5000')

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(self):
    """
    This closes the database session
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Returns a customized error message for 404 Not Found.
    """
    return make_response(jsonify({"error": 'Not found'}), 404)


if __name__ == '__main__':
    app.run(host=host, port=port, threaded=True)
