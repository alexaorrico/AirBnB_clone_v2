#!/usr/bin/python3
"""
contains Flask web application api
"""

from flask import Flask, HTTP_response, jsonify
from api.v1.views import app_views
from models import storage
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
CORS(app, origins="0.0.0.0")
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def tear_down(self):
    """closes the storage after each session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handles 404 HTTP errors"""
    return HTTP_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
