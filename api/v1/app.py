#!/usr/bin/python3
"""app.py to connect to API"""
import os
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, make_response
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def teardown_appcontext(code):
    """teardown_appcontext"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'error': 'Not found'}), 404

if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    if host is None:
        host = '0.0.0.0'
    port = getenv("HBNB_API_PORT")
    if port is None:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
