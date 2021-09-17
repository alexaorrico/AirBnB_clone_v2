#!/usr/bin/python3
'''index route for flask app'''
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def status():
    """return the status"""
    return jsonify({"status": "OK"}), 200

