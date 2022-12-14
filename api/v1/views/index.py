#!/usr/bin/python3
'''index one
'''

from api.v1.views import app_views
from flask import jsonify

app_views.route('/status')
def app_view():
    """just hoping this is a mistake"""
    
    return jsonify({"status": "OK"})