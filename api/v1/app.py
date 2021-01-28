#!/usr/bin/env python3
''' our first API '''

from flask import Flask, jsonify, make_response
from api.v1.views import app_views
from os import getenv
from models import storage

host = getenv('HBNB_API_HOST')
port = getenv('HBNB_API_PORT')

app = Flask(__name__)
app.register_blueprints(app_views)

@app.errorhandler(404)
def error_404(error):
    """Handling 404 error with JSON output"""
    return make_response(jsonify({"error": "Not found"})), 404


@app.teardown_appcontext
def storage_close(exception):
    """ Closes Storage with exception"""
    storage.close()


if __name__ == "__main__":
    if not host:
        host = '0.0.0.0'
    if not port:
        port = 5000
    app.run(host=host, debug=True, port=port, threaded=True)
