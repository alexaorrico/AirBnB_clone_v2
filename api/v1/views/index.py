#!/usr/bin/python3
"""index module"""
from api.v1.views import app_views
from models import storage


@app_views.route("/status")
def status():
    """returns the response status, OK"""
    return {"status": "OK"}


@app_views.route("/api/v1/stats")
def stats():
    """endpoint retrieves the number of each objects by type"""
    num = storage.count()
