#!/usr/bin/python3
"""Returns a JSON dict
"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status")
def status():
    return jsonify({"status": "OK"})
