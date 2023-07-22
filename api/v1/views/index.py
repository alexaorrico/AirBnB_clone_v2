#!/usr/bin/python3
""" this is the index.py file """
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def check_status():
    """ returns dict status: OK """
    return jsonify({"status": "OK"})
