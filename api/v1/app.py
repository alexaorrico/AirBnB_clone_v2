#!/usr/bin/python3
"""
initialization of app
"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_app_context
def shutdown(exception):
    """
    closes storage
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Return error in JSON and status"""
    return make_response(jsonify({"error":"Not Found"}), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = 5000
    app.run(host=host, port=port, threaded=True)
