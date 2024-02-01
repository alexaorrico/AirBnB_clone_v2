#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify

status = {
    "status": "OK",
}
@app_views.route('/status')
def status():
    """Returns status"""
    return jsonify(status)
