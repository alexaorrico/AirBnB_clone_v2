#!/usr/bin/python3
"""Flask RESTful API.

This initializes the Flask app for our AirBnB
Clone.

"""
import os
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Clear the storage and end the current session.

    Args:
        exception ('obj':'Exception'): Exception object.

    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handle the 404 Status Code Response.

    Args:
        error ('obj':'Error'): Error object.

    """
    error_response = jsonify({"error": "Not found"})
    error_response.status_code = 404
    return error_response


if __name__ == '__main__':
    app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    app_port = int(os.getenv('HBNB_API_PORT', 5000))
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.register_blueprint(app_views, url_prefix="/api/v1")
    app.run(host=app_host, port=app_port, threaded=True)
