#!/usr/bin/python3
"""imports app_views and routes /status on object app_view"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def app_status():
    ''' checks status of response '''
    return jsonify({"status": "OK"})
