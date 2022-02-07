#!/usr/bin/python3
""" Index.py """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def code_status():
    """ Show status of the code"""
    return jsonify({"status": "OK"})
