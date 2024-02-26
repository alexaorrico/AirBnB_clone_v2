#!/usr/bin/python3
"""Creates a lask web application API."""

from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
CORS(app, resources={r'/api/v1/*': {'origins': '0.0.0.0'}})
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_engine(exception):
    """removes all current SQLAlchemy session objects after each request."""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Return error message: "Not Found"."""
    response = {'error': 'Not Found'}
    return jsonify(response), 404


if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)
