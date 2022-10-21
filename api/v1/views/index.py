#!/usr/bin/python3
"""
Status of our Api and some stats.
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def app_status():
    """
    Simply returns the state of the api.
    """
    return(jsonify(status="OK"))


