#!/usr/bin/python3
"""
Flask module to return text as default route
"""
from flask import Flask, escape, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)


app.register_blueprint(app_views)


@app.teardown_appcontext
def close_app(self):
    '''close session'''
    storage.close()


@app.errorhandler(404)
def padge_not_found(e):
    '''handle unfound pages'''
    return make_response(jsonify({"error": "Not Found"}))


if __name__ == "__main__":
    h = '0.0.0.0'
    if getenv('HBNB_API_HOST'):
        h = getenv('HBNB_API_HOST')
    p = '5000'
    if getenv('HBNB_API_PORT'):
        p = getenv('HBNB_API_PORT')
    app.run(host=h, port=p, threaded=True)
