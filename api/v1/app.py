#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from werkzeug.exceptions import NotFound
from api.v1.views import app_views
from os import getenv
import json
import os

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(err):
    """API teardown function to close the storage"""
    from models import storage
    storage.close()


@app.errorhandler(404)
def not_found(err):
    """Error handler for 404 Not Found"""
    res = {'error': "Not found"}
    response = make_response(json.dumps(res), 404)
    response.headers['Content-Type'] = 'application/json'
    return response


@app.errorhandler(NotFound)
def handle_404_error(e):
    """Error handler for 404 Not Found using Werkzeug"""
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if __name__ == "__main__":
    """API entry point"""
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)

