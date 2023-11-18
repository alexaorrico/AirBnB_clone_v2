#!/usr/bin/python3
""" API Status Route """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """ Status Route Method """
    api_status = {"status": "OK"}
    return jsonify(api_status)
