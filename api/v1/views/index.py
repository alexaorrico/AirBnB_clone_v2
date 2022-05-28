#!/usr/bin/python3
""" Index view """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Return the status of your API """
    return jsonify({"status": "OK"})
