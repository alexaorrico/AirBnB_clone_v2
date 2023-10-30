#!/usr/bin/python3
"""Flask Application
This script creates a Flask application with the following features:
- Registers the app_views blueprint from api.v1.views
- Implements a method to handle app.teardown_appcontext, which calls storage.close()
- Runs the Flask server with configurable host and port values.
"""

from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask
from flask_cors import CORS

# Define default values for host and port
DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = '5000'

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_db(error):
    """Close Database Connection
    This function is called when the application context is torn down, and it
    ensures that
    the database connection is closed properly.
    Args:
        error: An error, if any, that occurred during the app context teardown.
    """
    storage.close()


if __name__ == "__main__":
    # Get host and port from environment variables or use defaults
    host = environ.get('HBNB_API_HOST', DEFAULT_HOST)
    port = environ.get('HBNB_API_PORT', DEFAULT_PORT)

    app.run(host=host, port=port, threaded=True)
