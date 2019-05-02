#!/usr/bin/python3
"""Starts flask"""
from flask import Flask, make_response, jsonify
from flask_cors import CORS, cross_origin
from models import storage
from api.v1.views import app_views
import os
app = Flask(__name__)
app.register_blueprint(app_views)
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)
CORS(app)


@app.teardown_appcontext
def tear_down(exc=None):
    """Tears down the application"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """404 not found response"""
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.run(host=host, port=port, threaded=True)
