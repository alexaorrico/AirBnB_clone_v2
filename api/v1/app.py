#!/usr/bin/python3
"""
This Flask app serves as the server-side component of a client-server
integration. It provides API endpoints and serves as the backend for
the client application. The app is configured to handle CORS
(Cross-Origin Resource Sharing) requests,
making it accessible from different origins.
"""
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

host = getenv("HBNB_API_HOST", '0.0.0.0')
port = getenv("HBNB_API_PORT", 5000)

app = Flask(__name__)
app.register_blueprint(app_views)
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
    app.run(host=host, port=port, threaded=True)
