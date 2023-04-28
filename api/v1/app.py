#!/usr/bin/python3
"""This is the API's application module"""

frrom api.vi.views import app_views
from flask import Flask, jsonify, make_response
from models import storage
import os

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def close_storage(exception):
    """function to handle teardown context"""
    storage.close()


@app.errorhandler(404)
def not_found(exception):
    """function to handle errors"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST') or '0.0.0.0'
    port = os.getenv('HBNB_API_PORT') or 5000
    app.run(host=host, port=port, threaded=True, debug=True)
