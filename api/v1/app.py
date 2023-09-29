#!/usr/bin/python3
"""api end point
"""

from os import getenv
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views

# create an instance of Flask
app = Flask(__name__)

#register the blueprint app_views to app
app.register_blueprint(app_views)

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
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", "5000"))

    # Run the Flask app with threads
    app.run(host=host, port=port, threaded=True, debug=True)
