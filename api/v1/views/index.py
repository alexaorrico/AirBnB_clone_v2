#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """
    The function "status" returns a JSON object
    with the key "status" set to "ok".
    """
    arg = {
        "status": "ok"
          }
    return jsonify(**arg)
