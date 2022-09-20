#!/usr/bin/python3
"""
flask application module
"""

from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status')
def jsonStatus():
    return jsonify(status=' ok')
