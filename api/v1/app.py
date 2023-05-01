#!/usr/bin/python3
"""
app installation
"""

# Import necessary libraries
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from flask_cors import CORS
from dotenv import load_dotenv
from os import getenv

load_dotenv() # load the env variables


# Create Flask instance
app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

# Register the blueprint app_views to the Flask instance
app.register_blueprint(app_views)


# Declare method to handle teardown_appcontext
@app.teardown_appcontext
def teardown_db_connection(exception):
    storage.close()


@app.errorhandler(404)
def handle_404_error(err):
    """Return the 404 JSON error message"""
    return jsonify(error='Not found'), 404


if __name__ == "__main__":
    # Run the Flask server
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
