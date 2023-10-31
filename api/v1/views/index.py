#!/usr/bin/python3
"""This module defines routes in the application"""

from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('status')
def return_status():
    """ returns a json response """
    return jsonify({"status": "OK"})
