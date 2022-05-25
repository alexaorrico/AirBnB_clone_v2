#!/usr/bin/python3
"""status of an api"""

from flask import Flask, jsonify
from models import storage
from api.v1.views.index.py import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """method to close a session"""
    storage.close()


@app.errorhandler(404)
def errorhandler(error):
    """method to handle 404 error"""
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    if getenv('HBNB_API_HOST'):
        jost = getenv('HBNB_API_HOST')
    else:
        jost = '0.0.0.0'
    if getenv('HBNB_API_PORT'):
        puerto = getenv('HBNB_API_PORT')
    else:
        puerto = 5000
    app.run(host=jost, port=puerto, threaded=True, debug=True)
