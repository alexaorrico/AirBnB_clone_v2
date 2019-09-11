#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def view_json():
    """
    Return the current status in a JSON file form
    """
    return jsonify({"status": "OK"})

