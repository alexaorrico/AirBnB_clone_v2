#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 14:42:23 2020
@authors: Robinson Montes
          Mauricio Olarte
"""
from os import getenv
from flask import Flask, jsonify, Blueprint
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="0.0.0.0")
app.register_blueprint(app_views)
CORS(app_views)


@app.teardown_appcontext
def close_db_sesion(error):
    """ this for slash routing"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """handler for 404 errors that returns a JSON-formatted
    404 status code response.
    """
    return ({'error': 'Not found'}), 404


if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT,
            threaded=True, debug=True)
