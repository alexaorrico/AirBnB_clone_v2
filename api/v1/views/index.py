#!/usr/bin/python3
""" index file """

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    """ status function """
    return jsonify({"status": "OK"})
