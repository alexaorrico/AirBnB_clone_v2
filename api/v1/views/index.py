#!/usr/bin/python3
"""
Create a route that returns a JSON
"""
from flask import Flask
from api.v1.views import app_views


@app_views.route('/api/v1/status', strict_slashes=False)
def return_status():
    """ returns a JSON """
    return {"status": "OK"}
