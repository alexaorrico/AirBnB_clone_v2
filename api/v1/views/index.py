#!/usr/bin/python3
"""Creates routes"""

from api.v1.views import app_views
from flask import jsonify, make_response


@app_views.route('/status')
def status():
    """Returns json rep of response code"""
    return make_response(jsonify({"status": "OK"}), 200)
