#!/usr/bin/python3
"""flask app"""

from os import getenv
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(excp):
    """Closes storage session"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """page not found"""
    return make_response(jsonify({'error': 'Not found'}), 400)


if __name__ == '__main__':
    api_host = getenv('HBNB_API_HOST')
    api_port = getenv('HBNB_API_PORT')
    if not api_host:
        api_host = '0.0.0.0'
    if not api_port:
        api_port = '5000'
    app.run(host=api_host, port=api_port, threaded=True)
