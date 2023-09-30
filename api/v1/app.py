#!/usr/bin/python3
"""api end point
"""

from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

# create an instance of Flask
app = Flask(__name__)

# register the blueprint app_views to app
app.register_blueprint(app_views)

# add CORS to the setup
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """closes the current session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """errors that returns a JSON-formatted
       404 status code response.
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    # Get the host and port from environment variables,
    # or use defaults if not defined
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")

    host = '0.0.0.0' if not host else host
    port = 5000 if not port else port

    # Run the Flask app with threads
    app.run(host=host, port=port, threaded=True)
