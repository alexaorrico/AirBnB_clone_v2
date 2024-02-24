#!/usr/bin/python3
"""Pending documentation"""
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """return OK status"""
    return {"status": "OK"}
