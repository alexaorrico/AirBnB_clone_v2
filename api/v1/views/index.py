#!/usr/bin/python3
""" Index Module"""

from api.v1.views import app_views
import json

@app_views.route("/status")
def status():
    status = {"status": "OK"}
    return (json.dumps(status))
