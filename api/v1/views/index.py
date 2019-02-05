#!/usr/bin/python3
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """ Returns the status of the http which should be 200 """
    return (jsonify({"status":"OK"}))

