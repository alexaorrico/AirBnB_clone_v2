#!/usr/bin/python3
"""
script that starts a Flask web application:
"""
from os import error, getenv
from models import storage
from api.v1.views import app_views
from flask import Blueprint, render_template, abort
from flask import Flask, jsonify, Response, make_response


app = Flask(__name__)
app.register_blueprint(app_views)

hbnb_api_host = getenv('HBNB_API_HOST', default='0.0.0.0')
hbnb_api_port = getenv('HBNB_API_PORT', default=5000)


@app.teardown_appcontext
def teardown(self):
    """
        method to handle teardown
    """
    storage.close()


@app.errorhandler(404)
def resource_not_found():
    """ Not found
    """
    mensaje = {'error': 'Not found'}
    return (jsonify(mensaje))


if __name__ == '__main__':
    app.run(host=hbnb_api_host, port=int(hbnb_api_port), threaded=True)
