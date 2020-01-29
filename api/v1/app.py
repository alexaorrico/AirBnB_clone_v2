#!/usr/bin/python3
"""
    API
"""
from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views
from models import storage
import os

app = Flask(__name__)

app.register_blueprint(app_views, url_prefix="/api/v1")
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def teardown_app(code):
    '''
       Method  Handles teardown
    '''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    '''
        handler for 404 errors that returns a JSON-formatted 404.
    '''
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
