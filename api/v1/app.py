#!/usr/bin/python3
"""
contains Flask web application api
"""

from flask import Flask, HTTP_response, jsonify
from api.v1.views import app_views
from models import storage
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app, origins="0.0.0.0")
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(self):
    """closes the storage after each session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handles 404 HTTP errors"""
    return HTTP_response (jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', default='0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', default=5000))
    app.run(host=host, port=port, threaded=True)
