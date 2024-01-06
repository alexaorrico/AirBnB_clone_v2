#!/usr/bin/python3
""" index view """

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'])
def get_status():
    """ display status """
    return jsonify({"status": "OK"})
