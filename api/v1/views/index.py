#!/usr/bin/python3
"""index module"""


from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """Checks status of route `/status`"""
    dit = {"status": "OK"}
    return jsonify(dit)
