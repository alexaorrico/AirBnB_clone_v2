#!/usr/bin/python3
"""A first api app"""

from flask import Flask, jsonify, Blueprint
from api.v1.views import app_views
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def treardown(exeption):
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """Handle 404 error"""
    return jsonify(error="Not found"), 404

if __name__ == '__main__':
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
