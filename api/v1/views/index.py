#!/usr/bin/python3
"""variable app_views which is an instance of Blueprint"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """status api"""
    new_dict = {}
    new_dict['status'] = "ok"
    return jsonify(new_dict)
