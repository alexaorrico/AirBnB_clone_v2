#!/usr/bin/python3
"""module containing a Flask Blueprint instance routes"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """returns a JSON"""
    return jsonify({"status": "OK"})
