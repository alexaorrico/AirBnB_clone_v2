i#!/usr/bin/python3
"""index status blueprint"""
from api.v1.views import app_views
from flask import jasonify
from models import storage

@app_views.route("/status")
def status():
    """check status"""
    return jasonify(status='OK')

@app_views.route("/api/v1/stats")
def stats():
    """checks the stats of each object by its type"""
    return jasonify(storage.count())

@app_views.errorhandler(404)
def not_found():
    """handles not found error"""
    response = jasonify(error='Not Found')
    response.status_code = 404
    return response
