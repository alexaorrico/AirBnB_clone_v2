#!/usr/bin/python3
"""
"""
from flask import Flask
from api.v1.views import app_views


@app_views.route("/status")
def api_status():
    """
    Returns status of API
    """
    return {"status": "ok"}
