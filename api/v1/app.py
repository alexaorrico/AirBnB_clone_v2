#!/usr/bin/python3
"""Main application script for a Flask-based API"""

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

# Create a Flask app instance
app = Flask(__name)

# Enable Cross-Origin Resource Sharing (CORS) for the API endpoints
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

# Configure URL routing to be less strict about trailing slashes
app.url_map.strict_slashes = False

# Register the blueprint for API views
app.register_blueprint(app_views)

# Define a function to be called when the application context is torn down
@app.teardown_appcontext
def close_storage(self):
    '''Closes the database storage engine'''
    storage.close()

# Define an error handler for 404 Not Found errors
@app.errorhandler(404)
def not_found(error):
    '''Handles 404 error and returns a JSON-formatted response'''
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    # Set the API host and port based on environment variables or use default values
    if getenv("HBNB_API_HOST") is None:
        HBNB_API_HOST = '0.0.0.0'
    else:
        HBNB_API_HOST = getenv("HBNB_API_HOST")
    
    if getenv("HBNB_API_PORT") is None:
        HBNB_API_PORT = 5000
    else:
        HBNB_API_PORT = int(getenv("HBNB_API_PORT"))

    # Start the Flask application with the specified host and port
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
