#!/usr/bin/python3
"""Definition for /status route to check API status"""


from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def get_status():
    return jsonify({"status": "OK"})
