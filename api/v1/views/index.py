#!/usr/bin/python3
"""Returns a Json response"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status")
def status_message():
    '''Returns status code'''
    return jsonify({"status": "OK"})

