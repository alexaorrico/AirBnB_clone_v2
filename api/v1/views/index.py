#!/usr/bin/python3
"""
module that is used for api index page
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', methods=['GET'])
def api_status():
    """ returns json string when request api status"""
    return jsonify({"status": "OK"})
