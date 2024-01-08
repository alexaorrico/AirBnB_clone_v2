#!/usr/bin/python3
'''
    Main application script for starting a Flask API with a registered blueprint.
'''

from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv


# Create a Flask application instance
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for the entire app
CORS(app, origins="0.0.0.0")

# Register the blueprint containing API views
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    '''
    Closes the database session after each request.
    '''
    storage.close()


@app.errorhandler(404)
def handle_not_found_error(error):
    '''
    Error handler for 404 Not Found status code.
    Returns a JSON-formatted 404 response.
    '''
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    # Run the Flask application
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", "5000"))
    app.run(host=host, port=port, threaded=True)
