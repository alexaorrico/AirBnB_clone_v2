#!/usr/bin/python3
"""
returns the status of the app_views object at route /status
"""

from . import app_views
from json import dumps


@app_views.route("/status")
def status():
    return dumps({"status": "OK"})
