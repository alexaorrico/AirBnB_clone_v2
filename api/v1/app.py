#!/usr/bin/python3
"""AirBnB Clone API configuration file"""

from flask import Flask, render_template, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)


# Register the blueprint
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_app(exception):
    """disconnect the db session """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """route for not found page"""
    err = {
        "error": "Not Found"
    }
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True)
