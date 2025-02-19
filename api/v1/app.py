#!/usr/bin/python3
"""Create a JSON 404 error page."""

from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, make_response
import os


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(exc):
    """Cleans up after the response"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Returns a JSON-formatted 404 status code"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))

    app.run(host=host, port=port, threaded=True, debug=True)
