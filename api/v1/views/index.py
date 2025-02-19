#!/usr/bin/python3
""" create routes """

from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'])
def status():
    """ route for status page """
    return jsonify({"status": "OK"})