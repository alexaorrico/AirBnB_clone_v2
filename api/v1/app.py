#!/usr/bin/python3
"""registers app using blueprint in flask"""
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from os import getenv
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """closes storage"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """handle 404 error"""
    return jsonify(error='Not found'), 404


if __name__ == '__main__':
    app.run(
        host=getenv('HBNB_API_HOST', '0.0.0.0'),
        port=getenv('HBNB_API_PORT', '5000'),
        threaded=True)
