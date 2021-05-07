#!/usr/bin/python3
"""Index file that returns a JSON status"""

from api.v1.views import app_views
from flask import Flask
from flask import jsonify


@app_views.route('/status')
def status():
    """Method that returns a JSON status"""
    return jsonify(status='OK')
