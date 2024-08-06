#!/usr/bin/python3
""" This module defines the root page from our Flask API """

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Returns the API status  """
    return jsonify({"status": "OK"})
