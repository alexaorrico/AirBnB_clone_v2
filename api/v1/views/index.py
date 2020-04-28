#!/usr/bin/python3
""" index """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ returns a JSON """
    return jsonify({"status": "OK"})
