#/usr/bin/python3
""" Routes of app.py """

from api.v1.views import app_views
from flask import make_response, Flask, jsonify, Blueprint
from json import dumps
from models import storage


@app_views.route("/status", strict_slashes=False)
def json_ok():
    """ Return the status of the api """
    response = make_response({"status": "ok"})
    response.headers['Content-Type'] = 'application/json'
    return response
