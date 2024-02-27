#!/usr/bin/python3
"""
flask app
"""
import os
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


# Create a Flask application instance
app = Flask(__name__)

# Register the blueprint app_views
app.register_blueprint(app_views)

# Initialize CORS with the app instance
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


# Declare a method to handle teardown
@app.teardown_appcontext
def teardown(exception):
    """
    teardown
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """
    page 404 Not found
    """
    return ({'error': 'Not found'}), 404


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    # getenv returns a string and port is an int
    # THREADED is set to true so it can serve multiple requests at once
    app.run(host=host, port=port, threaded=True)
