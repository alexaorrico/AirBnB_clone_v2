#!/usr/bin/python3

""" Creating the API Script for the AirBnB Clone Project
"""


from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
import os


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown(exception):
    """
    Closes the storage connection after each request
    """
    storage.close()


@app.errorhandler(404)
def handle_error404(error):
    """
    Handler for 404 errors
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    # Check if HBNB_API_HOST is set, otherwise use '0.0.0.0'
    if os.getenv('HBNB_API_HOST') is not None:
        host = os.getenv('HBNB_API_HOST')
    else:
        host = '0.0.0.0'
    # Check if HBNB_API_PORT is set, otherwise use port 5000
    if os.getenv('HBNB_API_PORT') is not None:
        port = os.getenv('HBNB_API_PORT')
    else:
        port = 5000
    # Run the Flask app
    app.run(host=host, port=port, threaded=True)
