#!/usr/bin/python3
'''
Create a Flask app and register the blueprint app_views to Flask instance app.
'''

# Import necessary modules
from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

# Create a Flask application instance
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for the app
CORS(app, resources={r'/api/v1/*': {'origins': '0.0.0.0'}})

# Register the app_views blueprint with the Flask app
app.register_blueprint(app_views)

# Disable strict slashes at the end of routes
app.url_map.strict_slashes = False

# Define a teardown function for cleaning up after each request
@app.teardown_appcontext
def teardown_engine(exception):
    '''
    Removes the current SQLAlchemy Session object after each request.
    '''
    storage.close()

# Define an error handler for 404 Not Found errors
@app.errorhandler(404)
def not_found(error):
    '''
    Return error message 'Not Found'.
    '''
    response = {'error': 'Not found'}
    return jsonify(response), 404

if __name__ == '__main__':
    # Get the host and port values from environment variables or use default values
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    
    # Run the Flask app
    app.run(host=HOST, port=PORT, threaded=True)
