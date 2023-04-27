#!/usr/bin/python3
"""Index"""


from models import storage
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """ API status"""
    return jsonify({"status": "OK"})
