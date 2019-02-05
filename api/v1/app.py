#!/usr/bin/python3
"""Endpint that returns the status of the API"""
from models import storage
from flask import Flask, render_template, jsonify, Blueprint
from api.v1.views import app_views
from os import environ
app = Flask(__name__)
app.register_blueprint(app_views)
app.config.update(JSONIFY_PRETTYPRINT_REGULAR=True)


@app.teardown_appcontext
def teardown(error):
    storage.close()


@app_views.route('/', strict_slashes=False)
def not_found(404):
    """ Gives the 404 not found page """
    return (jsonify({"error": "Not found"}), 404)

if __name__ == '__main__':
    if not environ.get('HBNB_API_HOST'):
        environ['HBNB_API_HOST'] = '0.0.0.0'
    if not environ.get('HBNB_API_PORT'):
        environ['HBNB_API_HOST'] = '5000'
    app.run(host=environ['HBNB_API_HOST'],
            port=environ['HBNB_API_PORT'],
            threaded=True)
