#!/usr/bin/python3
"""
initialize the package
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def jsonok():
    """return JSON"""
    return jsonify({"status":"OK"})
