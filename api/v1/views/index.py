#!/usr/bin/python3
"""Doc"""
from views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def index():
    """ returns a JSON """
    return jsonify(status="OK")
