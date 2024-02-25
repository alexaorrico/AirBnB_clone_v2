#!/usr/bin/python3
"""
contains status and  endpoints
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status_json():
    ''' route returning status page '''
    return jsonify({"status": "OK"})


