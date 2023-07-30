#!/usr/bin/python3
"""Flask API config file"""

from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from models import storage
import os

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_app(exception):
    """
    disconnects db session
    """
    storage.close


@app.errorhandler(404)
def error_404(error):
    """handles 404 error"""
    return jsonify(error='Not found'), 404


@app.errorhandler(400)
def error_400(error):
    """handles http 400 error code"""
    err = 'BAd request'
    if isinstance(error, Exception) and hasattr(error, 'description'):
        err = error.description
    return jsonify(error=err), 400


if __name__ == '__main__':
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port)
