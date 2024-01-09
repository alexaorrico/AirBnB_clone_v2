#!/usr/bin/python3
""" index module"""

from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False, methods=['GET'])
def status():
    return {
        "status": "OK"
    }
