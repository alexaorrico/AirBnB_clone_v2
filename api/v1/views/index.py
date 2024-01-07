#!/usr/bin/python3
"""
module for api index page
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """ returns json string """
    return jsonify({"status": "OK"})

