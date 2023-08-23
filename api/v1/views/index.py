#!/usr/bin/python3
""" views in app_views """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def app_views_status():
    """ displays a status message """
    return jsonify({"status": "OK"})
