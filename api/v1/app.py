#!/usr/bin/python3
"""Flask server (variable app)"""

from flask import Flask, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def downtear(self):
    """A method that Closes the storage"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """This method is called if page not found"""
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
