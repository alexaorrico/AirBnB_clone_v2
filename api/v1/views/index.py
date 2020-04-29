#!/usr/bin/python3
"""
File index.py
"""


from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Return status"""
    return jsonify({"status": "OK"})
